# Song Info Finder

A Flask web application for finding and editing MP3 metadata using MusicBrainz, Last.fm, and YouTube Music APIs.

## Features

- 🎵 **MP3 Metadata Extraction**: Read existing metadata from MP3 files
- 🔍 **Multi-Source Search**: Search for song information using iTunes API
- 🖼️ **Cover Art Retrieval**: Get album covers from Last.fm and YouTube Music
- ✏️ **Metadata Editing**: Edit and save metadata back to MP3 files
- 🖼️ **Cover Art Embedding**: Embed cover art directly into MP3 files
- 🔄 **Real-time Refresh**: Update search results with edited metadata
- 📱 **Responsive UI**: Modern Bootstrap-based interface

## Project Structure

```
music_finder/
├── main.py                 # Application entry point
├── app.py                  # Legacy entry point (deprecated)
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── music/                 # Main application package
│   ├── __init__.py        # Flask app factory
│   ├── config.py          # Configuration settings
│   ├── routes.py          # Flask route handlers
│   ├── modules.py         # Audio metadata classes
│   ├── services/          # External API services
│   │   ├── __init__.py
│   │   ├── http_service.py
│   │   ├── iteuns_api.py
│   │   └── musicbrainz_service.py
│   └── utils/             # Utility functions
│       ├── __init__.py
│       ├── datetime.py
│       ├── files.py
│       ├── logger.py
│       └── thumbnail.py
├── templates/             # HTML templates
│   ├── index.html
│   └── results.html
├── static/                # Static assets
│   └── style.css
├── tests/                 # Unit tests
└── uploads/               # Upload directory
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/MosaAmran11/music-finder.git
   cd music_finder
   ```

2. **Create a virtual environment**:
   1. On Windows:

   ```cmd
   py -m venv .venv
   .\.venv\Scripts\activate.bat
   ```

   2. On Linux:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys** (optional):
   Edit `music/config.py` to add your own API keys:

   ```python
   LASTFM_API_KEY = "your_lastfm_api_key"
   YOUTUBE_API_KEY = "your_youtube_api_key"
   ```

## Usage

### Running the Application

**Recommended way** (using the new structure):

```bash
python main.py
```

**Legacy way** (deprecated):

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

### How to Use

1. **Upload a File**: Enter the path to an MP3 file on your system
2. **View Results**: The app will search for song information and display matches
3. **Edit Metadata**: Click on any match to populate the form fields
4. **Save Changes**: Click "Save Metadata" to write changes back to the file
5. **Refresh Search**: Use the "Refresh" button to search with updated metadata

## Configuration

### Environment Variables

- `SECRET_KEY`: Flask secret key (default: 'a_very_secret_key')
- `FLASK_DEBUG`: Enable debug mode (default: True)
- `FLASK_HOST`: Host to bind to (default: 127.0.0.1)
- `FLASK_PORT`: Port to bind to (default: 5000)

### API Configuration

The application uses the following APIs:

- **iTunes API**: For song information (no API key required)
- **Last.fm API**: For cover art (API key in config)
- **YouTube Music API**: For cover art fallback (API key in config)

## Development

### Project Architecture

The application follows a modular Flask structure:

- **Application Factory**: `music/__init__.py` creates the Flask app
- **Blueprint Routes**: `music/routes.py` contains all route handlers
- **Services**: External API integrations in `music/services/`
- **Models**: Audio metadata classes in `music/modules.py`
- **Utilities**: Helper functions in `music/utils/`

### Adding New Features

1. **New Routes**: Add to `music/routes.py`
2. **New Services**: Create in `music/services/`
3. **New Utilities**: Add to `music/utils/`
4. **Configuration**: Update `music/config.py`

### Testing

Run the test suite:

```bash
python -m pytest tests/
```

## API Endpoints

- `GET /`: Main page for file upload
- `POST /`: Process uploaded file and search for metadata
- `POST /save_metadata`: Save metadata to MP3 file
- `POST /refresh_metadata`: Refresh search results (AJAX)

## Dependencies

- **Flask**: Web framework
- **mutagen**: MP3 metadata handling
- **requests**: HTTP client for API calls
- **Pillow**: Image processing for thumbnails

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **File not found**: Ensure the MP3 file path is correct and accessible
2. **No search results**: Check your internet connection and API keys
3. **Permission errors**: Ensure the app has write permissions for the MP3 file
4. **Cover art not embedding**: Check if the thumbnail URL is accessible

### Debug Mode

Enable debug mode for detailed error messages:

```bash
export FLASK_DEBUG=True
python main.py
```
