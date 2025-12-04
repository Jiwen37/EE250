from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# In-memory storage for simplicity
data_entries = []

@app.route('/')
def index():
    # Render HTML page with the data
    return render_template('index.html', entries=data_entries)

@app.route('/add', methods=['POST'])
def add_entry():
    """
    Expects JSON like: {"text": "Hello world", "frequency": 440}
    """
    entry = request.get_json()
    if entry and "text" in entry and "frequency" in entry:
        # Add the new entry
        data_entries.append({
            "text": entry["text"],
            "frequency": entry["frequency"]
        })
        return {"status": "success"}, 200
    else:
        return {"status": "error", "message": "Invalid data"}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
