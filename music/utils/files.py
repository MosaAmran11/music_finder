import tempfile


def create_temp_file(content, suffix='.mp3'):
    """
    Create a temporary file with the given content and suffix.

    :param content: The content to write to the temporary file.
    :param suffix: The suffix for the temporary file (default is '.mp3').
    :return: The path to the created temporary file.
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    with open(temp_file.name, 'wb') as f:
        f.write(content)
    return temp_file.name
