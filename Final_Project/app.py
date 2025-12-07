from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)
DATA_FILE = "entries.json"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                entries = json.load(f)
            except json.JSONDecodeError:
                entries = []
    else:
        entries = []
    return jsonify(entries)

#creating an entry
@app.route("/add_entry", methods=["POST"])
def add_entry():
    data = request.get_json()
    if not data or "text" not in data or "frequencies" not in data or "magnitudes" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    if len(data["frequencies"]) != len(data["magnitudes"]):
        return jsonify({"error": "Frequencies and magnitudes must have same length"}), 400

    entry = {
        "text": data["text"],
        "frequencies": data["frequencies"],
        "magnitudes": data["magnitudes"]
    }

    # Load existing entries
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                entries = json.load(f)
            except json.JSONDecodeError:
                entries = []
    else:
        entries = []

    entries.append(entry)

    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=2)

    return jsonify({"status": "success", "entry": entry}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6767, debug=True)



