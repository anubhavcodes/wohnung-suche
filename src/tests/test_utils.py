import pytest
from utils import validate_url


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
