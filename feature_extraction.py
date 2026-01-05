from urllib.parse import urlparse

SUSPICIOUS_WORDS = [
    "login", "verify", "bank", "secure",
    "account", "update", "confirm", "free"
]

def extract_features(url):
    features = {}

    features["url_length"] = len(url)
    features["count_dot"] = url.count(".")
    features["count_hyphen"] = url.count("-")
    features["count_at"] = url.count("@")
    features["count_slash"] = url.count("/")
    features["has_https"] = 1 if url.startswith("https") else 0

    features["suspicious_words"] = sum(
        word in url.lower() for word in SUSPICIOUS_WORDS
    )

    parsed = urlparse(url)
    features["subdomain_count"] = parsed.netloc.count(".")

    return features

