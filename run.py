from flask import Flask , render_template, request, jsonify
import json
import os

app = Flask(__name__)

HISTORY_FILE = 'history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as file:
            return json.load(file)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as file:
        json.dump(history, file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history', methods=['POST'])
def add_city():
    city = request.json.get('city')
    history = load_history()
    if city and city not in history:
        history.insert(0, city)  # most recent first
        if len(history) > 10:
            history = history[:10]
        save_history(history)
    return jsonify({'status': 'success'})

@app.route('/history_page')
def history_page():
    history = load_history()
    return render_template('history.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)