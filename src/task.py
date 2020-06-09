import logging
from typing import Dict, Tuple
from urllib.parse import urlparse

from app import app
from exception import CardNotFoundException, ConfigurationError
from trello import Trello
from utils import PROVIDERS, validate_url

logger = logging.getLogger(__name__)


def get_formatted_info(result: Dict) -> Tuple[str, str]:
    name = result["address"] or result["title"]
    desc = f"# {result['title']}\n\n"
    desc += f"**address**: {result['address']}\n**cold**: {result['cold_rent']}\n"
    desc += f"**warm**: {result['warm_rent']}\n**size**: {result['size']}\n"
    desc += f"**available from**: {result['available_from']}\n"
    desc += f"**construction year**: {result['construction_year']}"
    return name, desc.strip()


def process_card(card_id: str):
    if not all([app.config["TRELLO_TOKEN"], app.config["TRELLO_KEY"]]):
        raise ConfigurationError("Please set TRELLO API KEY and TRELLO SECRET")
    t = Trello(trello_key=app.config["TRELLO_KEY"], trello_token=app.config["TRELLO_TOKEN"])
    card = t.get_card(card_id=card_id)
    if not card:
        raise CardNotFoundException(f"Card with id {card_id} does not exists.")
    url = card["name"]
    if not validate_url(url):
        logger.info(f"Found a card without a valid url... skipping {card_id}: {url}")
    result = PROVIDERS[urlparse(url).netloc](url=url).scrape()
    if not result:
        raise ValueError(f"Unable to parse {url}... Check logs")
    name, desc = get_formatted_info(result)
    t.update_card(card_id=card_id, name=name, desc=desc)
    for attachment in result["images"]:
        t.add_attachment_to_card(card_id=card_id, attachment_url=attachment)
