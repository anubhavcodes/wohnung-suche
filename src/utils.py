import os
from urllib.parse import urlparse

from exception import EnvironmentVariableError


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


def get_environment_variable(key: str, type, default=None):
    try:
        value = os.environ.get(key, default=default)
        return type(value)
    except TypeError:
        raise TypeError(f"Error coercing {key} to {type}")
    except Exception as e:
        raise EnvironmentVariableError(f"Error reading {key} from the environment: {e}")


def configure_sentry():
    sentry_dsn = get_environment_variable("SENTRY_DSN", str, default=None)
    if sentry_dsn:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration

        sentry_sdk.init(dsn=sentry_dsn, integrations=[FlaskIntegration()])
