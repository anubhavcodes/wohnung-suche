from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/api", methods=["GET"])
def trello_webhook():
    url = request.args.get("url", None)
    if not url:
        return jsonify({"message": "Query param url is missing"}), 401
    else:
        return jsonify({"message": f"{url}"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
