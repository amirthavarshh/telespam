from flask import Flask, jsonify
from flask import request
from listener import set_channel
from flask_cors import CORS
import joblib
import re

app = Flask(__name__)
CORS(app)

# ---- AI MODEL ----
model = joblib.load("spam_model.pkl")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

# ---- DATA STORAGE ----
data_store = {
    "text": "Awaiting first transmission...",
    "status": "Waiting",
    "total": 0,
    "spam_count": 0,
    "normal_count": 0
}

# ---- API FOR WEBSITE ----
@app.route("/get_message")
def get_message():
    return jsonify(data_store)

# ---- FUNCTION CALLED BY TELEGRAM BOT ----
def update_message(text, status):
    global data_store

    data_store["text"] = text
    data_store["status"] = status
    data_store["total"] += 1

    if status == "SPAM":
        data_store["spam_count"] += 1
    else:
        data_store["normal_count"] += 1
        # ---- SELECT TELEGRAM CHANNEL FROM WEBSITE ----
# ---- SELECT TELEGRAM CHANNEL FROM WEBSITE ----
@app.route("/set_channel", methods=["POST"])
def select_channel():
    data = request.json
    channel = data.get("channel")

    set_channel(channel)

    return jsonify({
        "status": "connected",
        "channel": channel
    })


# ---- START SERVER ----
if __name__ == "__main__":
    app.run(port=5000)
