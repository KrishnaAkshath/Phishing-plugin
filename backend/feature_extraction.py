import re
from urllib.parse import urlparse

def extract_features(url):
    features = []

    parsed = urlparse(url)

    # Length features
    features.append(len(url))
    features.append(len(parsed.netloc))
    features.append(len(parsed.path))

    # Special character counts
    features.append(url.count('-'))
    features.append(url.count('@'))
    features.append(url.count('?'))
    features.append(url.count('%'))
    features.append(url.count('.'))

    # HTTPS check
    features.append(1 if parsed.scheme == "https" else 0)

    # IP address check
    ip_pattern = r"\b\d{1,3}(\.\d{1,3}){3}\b"
    features.append(1 if re.search(ip_pattern, url) else 0)

    return features

