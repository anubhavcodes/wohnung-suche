import os

from utils import get_environment_variable


class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    REDIS_URL = get_environment_variable("REDIS_URL", str, default="redis://")
    TRELLO_TOKEN = get_environment_variable("TRELLO_TOKEN", str, None)
    TRELLO_KEY = get_environment_variable("TRELLO_KEY", str, None)
