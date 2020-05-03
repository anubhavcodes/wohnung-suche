from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/trello", methods=["POST"])
def trello_webhook():
    print(request.data)
    return jsonify({"message": "okay"})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
