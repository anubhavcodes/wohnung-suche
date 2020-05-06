from flask import Flask, jsonify, request
from utils import validate_url

app = Flask(__name__)
app.config.from_object("config.Config")


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/api", methods=["GET"])
def trello_webhook():
    url = request.args.get("url", None)
    if not url:
        return jsonify({"message": "Query param url is missing"}), 401
    if not validate_url(url):
        return jsonify({"message": f"Invalid url: {url}"}), 402
    else:
        return jsonify({"message": f"{url}"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
