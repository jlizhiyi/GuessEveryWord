from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# wordlist from MIT
with open('wordlist.txt') as f:
    valid_words = set(word.strip().lower() for word in f if re.fullmatch(r'[a-z\-]*', word.strip().lower()))
valid_words = set(word.replace('-', '') for word in valid_words)

named_words = []
count = 0

@app.route('/check_word', methods=['POST'])
def check_word():
    global count, named_words
    word = request.json.get('word', '').strip().lower()

    if not word:
        return jsonify({'error': 'You did not enter a word. Try again.'}), 400

    if word not in valid_words:
        return jsonify({'error': f'"{word}" is not a valid English word. Try again.'}), 400

    if word in named_words:
        return jsonify({'error': f'You have already named "{word}". Try again.'}), 400

    named_words.append(word)
    count += 1

    return jsonify({
        'count': count,
        'last25Words': list(reversed(named_words[-25:])),
        'allWords': sorted(named_words)
    })

@app.route('/clear_data', methods=['POST']) 
def clear_data():
    global named_words, count
    named_words = [] # reset words array
    count = 0 # reset count
    return "Data cleared"

if __name__ == '__main__':
    app.run(debug=True)
