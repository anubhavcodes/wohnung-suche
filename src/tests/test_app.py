import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_base_url_returns_correct_status(client):
    rv = client.get("/")
    assert rv.status_code == 200


def test_webhook_url_returns_200_for_head_requests(client):
    rv = client.head("/webhook")
    assert rv.status_code == 200


def test_api_endpoint_returns_error_for_no_url(client):
    rv = client.get("/api")
    assert rv.status_code == 401


@pytest.mark.parametrize(
    "url", ["https://www.google.com", "https://www.facebook.com", "foo", "bar", "ftp://foo.bar", "localhost"]
)
def test_api_endpoint_returns_error_for_invalid_url(client, url):
    rv = client.get(f"/api?url={url}")
    assert rv.status_code == 402
    assert "Invalid url" in rv.json.get("message")
