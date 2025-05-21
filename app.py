import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from metadata_reader import extract_metadata
from musicbrainz_search import search_musicbrainz
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
import builtins  # Import builtins to access enumerate

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3'}

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
        if 'file' not in request.files:
            return render_template('index.html', error='No file part in the request.')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error='No selected file.')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # To keep the file for editing, save it with a unique name or in a persistent location
            # For this example, we'll save it temporarily and assume the user won't upload another
            # before editing. In a real app, you'd need a more robust file management strategy.
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            metadata = extract_metadata(filepath)
            results = []
            if metadata.get("title") and metadata.get("artist"):
                results = search_musicbrainz(
                    metadata["title"], metadata["artist"])

            # Do NOT remove the file here if we want to edit it later
            # os.remove(filepath)

            # Pass enumerate function to the template context
            return render_template('results.html', metadata=metadata, results=results, enumerate=builtins.enumerate)

        else:
            return render_template('index.html', error='Invalid file type. Only MP3 is allowed.')

    return render_template('index.html')


@app.route('/save_metadata', methods=['POST'])
def save_metadata():
    filepath = request.form.get('filepath')
    if not filepath or not os.path.exists(filepath):
        # Handle missing file or invalid path
        # In a real app, you'd want more secure path handling
        return "Error: File not found.", 404  # Or render an error template

    try:
        # Open the MP3 file and get ID3 tags
        # Use EasyID3 for simple tag manipulation
        audio = EasyID3(filepath)
    except ID3NoHeaderError:
        # If no ID3 header exists, create one
        audio = EasyID3()
        audio.save(filepath)  # Save the empty header
        audio = EasyID3(filepath)  # Re-open with the new header
    except Exception as e:
        print(f"Error opening file for editing: {e}")
        return "Error: Could not open file for editing.", 500

    # Get data from the form and update tags
    audio['title'] = request.form.get('title', '')
    audio['artist'] = request.form.get('artist', '')
    audio['album'] = request.form.get('album', '')
    audio['genre'] = request.form.get('genre', '')
    audio['tracknumber'] = request.form.get('tracknumber', '')
    audio['discnumber'] = request.form.get('discnumber', '')
    audio['lyrics'] = request.form.get('lyrics', '')
    audio['comment'] = request.form.get('comment', '')
    audio['albumartist'] = request.form.get('albumartist', '')
    audio['composer'] = request.form.get('composer', '')
    audio['date'] = request.form.get('date', '')  # Save as 'date' tag

    # Bitrate and filepath are not standard editable ID3 tags

    try:
        audio.save()
        print(f"Metadata saved for {filepath}")
        # Redirect back to the results page or a success page
        # For simplicity, redirect back to index for now.
        # In a real app, you might re-render the results page with saved data.
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error saving metadata: {e}")
        return "Error: Could not save metadata.", 500


if __name__ == '__main__':
    app.run(debug=True)
