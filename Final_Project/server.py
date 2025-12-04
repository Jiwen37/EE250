from flask import Flask, request, jsonify
import json
import os
from threading import Lock

app = Flask(__name__)

DATA_FILE = "data.json"
file_lock = Lock()  # prevents file corruption if many writes happen

def load_data():
    """Read and return the list of entries from data.json."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []  # fallback if file corrupts
            

def save_data(data):
    """Write the updated list back to data.json safely."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/add", methods=["POST"])
def add_entry():
    content = request.get_json()
    if not content or "text" not in content or "frequency" not in content:
        return jsonify({"error": "Missing 'text' or 'frequency'"}), 400

    text = content["text"]
    freq = content["frequency"]

    with file_lock:
        data = load_data()
        data.append({"text": text, "frequency": freq})
        save_data(data)

    return jsonify({"status": "ok", "message": "Entry added"}), 200

@app.route("/data", methods=["GET"])
def get_data():
    with file_lock:
        data = load_data()
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6767, debug=True)

