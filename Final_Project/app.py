from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)
file = "entries.json"

@app.route("/")
def index():
    return render_template("index.html")
#get all data in json file - easier for our purposes than getting one file at a time since we want to load everything every time
@app.route("/data")
def get_data():
    if not os.path.exists("entries.json") or os.path.getsize("entries.json") == 0:
        with open("entries.json", "w") as f:
            json.dump([], f)

    with open("entries.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
            with open("entries.json", "w") as fw:
                json.dump(data, fw)

    return jsonify(data)


#creating an entry
@app.route("/add_entry", methods=["POST"])
def add_entry():
    data = request.get_json()

    entry = {
        "text": data["text"],
        "frequencies": data["frequencies"],
        "magnitudes": data["magnitudes"]
    }

    with open(file, "r") as f:
        entries = json.load(f)

    entries.append(entry)

    with open(file, "w") as f:
        json.dump(entries, f, indent=2)

    return jsonify({"status": "success", "entry": entry}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6767, debug=True)



