"""
Song Info Finder - A Flask application for finding and editing MP3 metadata.
"""

from flask import Flask
import os


def create_app(config=None):
    """Application factory pattern for Flask app."""
    app = Flask(__name__)

    # Default configuration
    app.config.update(
        UPLOAD_FOLDER='uploads',
        SECRET_KEY='a_very_secret_key',
        ALLOWED_EXTENSIONS={'mp3'},
        SEARCH_TERMS=['title', 'artist', 'album']
    )

    # Override with custom config if provided
    if config:
        app.config.update(config)

    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Register blueprints
    from music.routes import main_bp
    app.register_blueprint(main_bp)

    return app
