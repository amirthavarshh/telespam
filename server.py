from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data_store = {
    "text": "No messages yet",
    "status": "Waiting",
    "spam_count": 0,
    "normal_count": 0,
    "total": 0
}

@app.route("/get_message")
def get_message():
    return jsonify(data_store)



def update_message(text, status):
    global data_store

    data_store["text"] = text
    data_store["status"] = status
    data_store["total"] += 1

    if status == "SPAM":
        data_store["spam_count"] += 1
    else:
        data_store["normal_count"] += 1


if __name__ == "__main__":
    app.run(port=5000)
