import logging
from urllib.parse import urlparse

from flask import Flask, jsonify, request
from flask_cors import CORS
from providers.immoscout import Immoscout
from providers.immowelt import Immowelt
from utils import configure_sentry, validate_url

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object("config.Config")

logger = logging.getLogger(__name__)
configure_sentry()


PROVIDERS = {"www.immowelt.de": Immowelt, "www.immobilienscout24.de": Immoscout}


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
    except Exception as e:
        raise e


if __name__ == "__main__":
    app.run(host="0.0.0.0")
