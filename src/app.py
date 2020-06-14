import logging
from urllib.parse import urlparse

import rq
from config import Config
from flask import Flask, jsonify, request
from flask_cors import CORS
from redis import Redis
from utils import PROVIDERS, configure_sentry, validate_url

app = Flask(__name__)
app.config.from_object(Config)
app.redis = Redis.from_url(app.config["REDIS_URL"])
app.task_queue = rq.Queue("cardupdater", connection=app.redis)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

logger = logging.getLogger(__name__)
configure_sentry()


@app.route("/")
def health_check():
    return jsonify({"message": "Status OK", "details": "This is not where you should be."})


@app.route("/api", methods=["GET"])
def api():
    url = request.args.get("url", None)
    if not url:
        return jsonify({"message": "Query param url is missing"}), 401
    if not validate_url(url):
        return jsonify({"message": f"Invalid url: {url}"}), 402
    try:
        result = PROVIDERS[urlparse(url).netloc](url=url).scrape()
        if result:
            return jsonify({"message": "Success", "url": url, "result": result}), 200
    except KeyError as e:
        logger.debug(f"Unable to extract the provider from the url: {url}")
        raise e
    except Exception as e:
        raise e


@app.route("/webhook", methods=["POST", "HEAD"])
def webhook():
    if request.method == "HEAD":
        return jsonify({"message": "Hello Trello!!! This api works."}), 200
    action = request.json.get("action")
    card_id = None
    if action["type"] == "createCard":
        board = action["data"].get("board")
        if board:
            card = action["data"].get("card")
        if card:
            card_id = card.get("id")
    if not card_id:
        return jsonify({"message": "card not found", "action": action})
    app.task_queue.enqueue("task.process_card", card_id)
    return jsonify({"message": "queued"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
