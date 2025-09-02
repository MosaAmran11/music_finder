"""
Configuration settings for the Song Info Finder application.
"""

import os

# Application Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3'}
SEARCH_TERMS = ['title', 'artist', 'album']

# App Defaults
RESULTS_LIMIT_DEFAULT = int(os.environ.get('RESULTS_LIMIT_DEFAULT', 5))

# Flask Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_key')

# Development Configuration
DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
PORT = int(os.environ.get('FLASK_PORT', 5000))
