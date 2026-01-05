import re
from urllib.parse import urlparse

def extract_features(url):
    parsed = urlparse(url)

    return [
        len(url),
        url.count('.'),
        url.count('-'),
        url.count('@'),
        url.count('?'),
        url.count('%'),
        url.count('='),
        url.count('http'),
        url.count('https'),
        1 if parsed.scheme == "https" else 0
    ]
