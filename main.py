#!/usr/bin/env python3
"""
Entry point for the Song Info Finder application.
"""

from music import create_app
from music.config import DEBUG, HOST, PORT

app = create_app()

if __name__ == '__main__':
    app.run(
        debug=DEBUG,
        host=HOST,
        port=PORT
    )
