"""
Legacy app.py - Redirects to the new modular structure.
This file is kept for backward compatibility.
"""

from music import create_app
import warnings

warnings.warn(
    "app.py is deprecated. Use main.py instead.",
    DeprecationWarning,
    stacklevel=2
)


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
