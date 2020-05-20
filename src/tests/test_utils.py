import os

import pytest
from utils import get_environment_variable, validate_url


@pytest.mark.parametrize(
    "url",
    [
        "https://www.immobilienscout24.de/expose/118216960#/",
        "https://www.immowelt.de/expose/2vzau4e",
        "http://www.immobilienscout24.de/expose/118216960#/",
        "http://www.immowelt.de/expose/2vzau4e",
    ],
)
def test_validate_url_validates_correct_url(url):
    assert validate_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "www.immobilienscout24.de/expose/118216960#/",
        "www.immowelt.de/expose/2vzau4e",
        "https://www.google.com",
        "https://www.facebook.com",
        "foo",
        "bar",
        "ftp://foo.bar",
        "localhost",
    ],
)
def test_validate_url_returns_false_for_invalid_url(url):
    assert not validate_url(url)


def test_get_environment_variable():
    os.environ["FOO"] = "21"
    value = get_environment_variable("FOO", int)
    assert value == 21
    os.environ["FOO"] = "21"
    value = get_environment_variable("FOO", str)
    assert value == "21"
    assert get_environment_variable("BAR", int, default=22) == 22
    with pytest.raises(ValueError):
        os.environ["BAZ"] = "abcd"
        get_environment_variable("BAZ", type=int, default=None)
    assert not get_environment_variable("SENTRY_DSN", str, default=None)
