from pprint import pprint
from urllib.parse import urlparse

import click
from app import PROVIDERS
from utils import configure_sentry, validate_url

configure_sentry()


@click.command()
@click.argument("url")
def scrape(url):
    if not validate_url(url):
        click.echo(pprint({"message": f"Invalid url: {url}"}))
    try:
        result = PROVIDERS[urlparse(url).netloc](url=url).scrape()
        if result:
            click.echo(pprint(result))
    except Exception as e:
        raise (e)


if __name__ == "__main__":
    scrape()
