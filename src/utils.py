from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    """ A method to validate if the url if valid."""
    if not url.startswith("http"):
        return False
    try:
        result = urlparse(url)
        if not all([result.scheme in ["http", "https"], result.netloc, result.path]):
            return False
    except Exception:
        return False
    if result.netloc not in ["www.immowelt.de", "www.immobilienscout24.de"]:
        # @TODO: add a logger here and send the url to sentry
        return False
    return True
