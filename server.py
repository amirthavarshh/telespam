from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_message = {
    "text": "No messages yet",
    "status": "Waiting"
}

@app.route("/get_message")
def get_message():
    return jsonify(latest_message)

def update_message(text, status):
    global latest_message
    latest_message = {
        "text": text,
        "status": status
    }

if __name__ == "__main__":
    app.run(port=5000)
