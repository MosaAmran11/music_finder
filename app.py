import builtins  # Import builtins to access enumerate
import os

from flask import Flask, render_template, request, jsonify, render_template_string
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from requests.exceptions import ConnectionError

from music.modules import AudioTags, ExtendedAudioTags
from music.services.iteuns_api import get_song_info
from music.utils.thumbnail import embed_thumbnail, download_thumbnail

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3'}
SEARCH_TERMS = ['title', 'artist', 'album']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'a_very_secret_key'  # Needed for flashing messages

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filepath = request.form.get('filepath')
        is_refresh = request.form.get('refresh') == '1'

        if not filepath:
            return render_template('index.html', error='No file path provided.')

        if not os.path.exists(filepath):
            return render_template('index.html', error='File not found. Please check the path.')

        if not filepath.lower().endswith('.mp3'):
            return render_template('index.html', error='Invalid file type. Only MP3 files are allowed.')

        try:
            if is_refresh:
                # Use posted values for metadata
                metadata = AudioTags(filepath)
                # Overwrite with posted values
                for field in ['title', 'artist', 'album', 'genre', 'tracknumber', 'discnumber', 'albumartist', 'date']:
                    val = request.form.get(field)
                    if val is not None:
                        setattr(metadata, field, val)
            else:
                metadata = AudioTags(filepath)
            # Use the current metadata fields for searching
            search_terms = [metadata.get(t)
                            for t in SEARCH_TERMS if metadata.get(t)]
            song_info = get_song_info(search_terms)
            results = []
            for data in song_info:
                extend_audio = ExtendedAudioTags()
                extend_audio.itunes_parse(data)
                results.append(extend_audio.to_dict())
            print(metadata)
            print(results)
            return render_template('results.html', metadata=metadata, results=results, enumerate=builtins.enumerate)
        except ConnectionError:
            return render_template('index.html', error=f'No internet connection.')
        except Exception as e:
            return render_template('index.html', error=f'Error processing file: {str(e)}')
    return render_template('index.html')


@app.route('/save_metadata', methods=['POST'])
def save_metadata():
    filepath = request.form.get('filepath')
    thumbnail_url = request.form.get('thumbnailUrl')
    if not filepath or not os.path.exists(filepath):
        return ("Error: File not found.", 404) if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest' else render_template('results.html', metadata=None, results=[], error='File not found.')

    try:
        audio = EasyID3(filepath)
    except ID3NoHeaderError:
        audio = EasyID3()
        audio.save(filepath, v2_version=3)
        audio = EasyID3(filepath)
    except Exception as e:
        print(f"Error opening file for editing: {e}")
        return ("Error: Could not open file for editing.", 500) if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest' else render_template('results.html', metadata=None, results=[], error='Could not open file for editing.')

    audio['title'] = request.form.get('title', '')
    audio['artist'] = request.form.get('artist', '')
    audio['album'] = request.form.get('album', '')
    audio['genre'] = request.form.get('genre', '')
    audio['tracknumber'] = request.form.get('tracknumber', '')
    audio['discnumber'] = request.form.get('discnumber', '')
    audio['albumartist'] = request.form.get('albumartist', '')
    audio['date'] = request.form.get('date', '')

    try:
        audio.save(v2_version=3)
        print(f"Metadata saved for {filepath}")
        # Always embed cover art if thumbnailUrl is provided
        if thumbnail_url:
            try:
                thumb_path = download_thumbnail(thumbnail_url)
                embed_thumbnail(filepath, thumb_path)
                print(f"Thumbnail embedded for {filepath}")
            except Exception as e:
                print(f"Warning: Could not embed thumbnail: {e}")
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Metadata saved successfully.'})
        return render_template('results.html', metadata=AudioTags(filepath), results=[], success='Metadata saved successfully.')
    except Exception as e:
        print(f"Error saving metadata: {e}")
        return ("Error: Could not save metadata.", 500) if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest' else render_template('results.html', metadata=None, results=[], error='Could not save metadata.')


@app.route('/refresh_metadata', methods=['POST'])
def refresh_metadata():
    filepath = request.form.get('filepath')
    # Use the current form values for the search
    title = request.form.get('title', '')
    artist = request.form.get('artist', '')
    album = request.form.get('album', '')
    genre = request.form.get('genre', '')
    tracknumber = request.form.get('tracknumber', '')
    discnumber = request.form.get('discnumber', '')
    date = request.form.get('date', '')
    albumartist = request.form.get('albumartist', '')
    try:
        # Use the updated metadata fields for searching
        search_terms = [title, artist, album]
        song_info = get_song_info([t for t in search_terms if t])
        results = []
        for data in song_info:
            extend_audio = ExtendedAudioTags()
            extend_audio.itunes_parse(data)
            results.append(extend_audio.to_dict())
        # Create a temporary metadata object with the current form values
        metadata = AudioTags(filepath)
        for field, val in [('title', title), ('artist', artist), ('album', album), ('genre', genre), ('tracknumber', tracknumber), ('discnumber', discnumber), ('albumartist', albumartist), ('date', date)]:
            if val is not None:
                setattr(metadata, field, val)
        # Render only the #results-section as HTML
        results_html = render_template_string(
            '{% include "results.html" %}',
            metadata=metadata,
            results=results,
            enumerate=enumerate
        )
        # Extract only the #results-section div
        import re
        match = re.search(
            r'<div id="results-section">([\s\S]*?)</div>', results_html)
        section_html = '<div id="results-section">' + \
            match.group(1) + '</div>' if match else ''
        return jsonify({'success': True, 'html': section_html})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
