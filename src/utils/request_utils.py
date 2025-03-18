from typing import Any
from urllib.parse import parse_qs


def parse_form_data(environ: dict[str, Any]) -> dict[str, str]:
    """
    Parse form data from WSGI environ object.

    :param environ: WSGI environment dictionary
    :return: Dictionary with form field names as keys and their values as strings
    """
    content_length = int(environ.get('CONTENT_LENGTH', 0))
    post_data_bytes = environ['wsgi.input'].read(content_length).decode('utf-8')
    params = parse_qs(post_data_bytes)
    return {k: v[0] if v else '' for k, v in params.items()}