import re
import urllib.parse

def extract_features(url: str):
    parsed = urllib.parse.urlparse(url)

    features = [
        len(url),                              # URL length
        url.count('.'),                        # number of dots
        url.count('-'),                        # hyphens
        url.count('@'),                        # @ symbol
        url.count('?'),                        # query params
        url.count('='),                        # equals
        url.count('/'),                        # slashes
        url.count('%'),                        # encoding
        url.count('http'),                     # http occurrences
        1 if parsed.scheme == "https" else 0, # HTTPS?
        len(parsed.netloc),                    # domain length
        1 if re.search(r"(login|verify|secure|account|bank)", url.lower()) else 0
    ]

    return features
