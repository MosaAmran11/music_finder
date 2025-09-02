"""
Flask routes for the Song Info Finder application.
"""

import builtins
import re
import os
from flask import Blueprint, render_template, request, jsonify, render_template_string, current_app, session, redirect, url_for
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from requests.exceptions import ConnectionError

from music.modules import AudioTags, ExtendedAudioTags
from music.services.itunes_api import get_song_info
from music.config import RESULTS_LIMIT_DEFAULT
from music.utils.thumbnail import embed_thumbnail, download_thumbnail

main_bp = Blueprint('main', __name__)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    """Main route for file upload and processing."""
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
            search_terms = [metadata.get(
                t) for t in current_app.config['SEARCH_TERMS'] if metadata.get(t)]
            # Determine results limit from session or default
            results_limit = session.get('results_limit', RESULTS_LIMIT_DEFAULT)
            song_info = get_song_info(search_terms, limit=results_limit)
            results = []
            for data in song_info:
                extend_audio = ExtendedAudioTags()
                extend_audio.itunes_parse(data)
                results.append(extend_audio.to_dict())

            return render_template('results.html', metadata=metadata, results=results, enumerate=builtins.enumerate)
        except ConnectionError:
            return render_template('index.html', error='No internet connection.')
        except Exception as e:
            return render_template('index.html', error=f'Error processing file: {str(e)}')

    return render_template('index.html')


@main_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    """Settings page to configure UI preferences."""
    if request.method == 'POST':
        try:
            results_limit = int(request.form.get(
                'results_limit', RESULTS_LIMIT_DEFAULT))
            if results_limit < 1:
                results_limit = RESULTS_LIMIT_DEFAULT
        except (TypeError, ValueError):
            results_limit = RESULTS_LIMIT_DEFAULT

        session['results_limit'] = results_limit
        # After saving, redirect back to index or referer
        return redirect(url_for('main.index'))

    current_limit = session.get('results_limit', RESULTS_LIMIT_DEFAULT)
    return render_template('settings.html', current_limit=current_limit)


@main_bp.route('/save_metadata', methods=['POST'])
def save_metadata():
    """Save metadata to MP3 file."""
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

    # Update metadata fields
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

        # Embed cover art if thumbnailUrl is provided
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


@main_bp.route('/refresh_metadata', methods=['POST'])
def refresh_metadata():
    """Refresh metadata search results."""
    filepath = request.form.get('filepath')

    # Get current form values for the search
    form_fields = ['title', 'artist', 'album', 'genre',
                   'tracknumber', 'discnumber', 'date', 'albumartist']
    form_data = {field: request.form.get(field, '') for field in form_fields}

    try:
        # Use the updated metadata fields for searching
        search_terms = [form_data['title'],
                        form_data['artist'], form_data['album']]
        song_info = get_song_info([t for t in search_terms if t])
        results = []
        for data in song_info:
            extend_audio = ExtendedAudioTags()
            extend_audio.itunes_parse(data)
            results.append(extend_audio.to_dict())

        # Create a temporary metadata object with the current form values
        metadata = AudioTags(filepath)
        for field, val in form_data.items():
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
        match = re.search(
            r'<div id="results-section">([\s\S]*?)</div>', results_html)
        section_html = '<div id="results-section">' + \
            match.group(1) + '</div>' if match else ''

        return jsonify({'success': True, 'html': section_html})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
