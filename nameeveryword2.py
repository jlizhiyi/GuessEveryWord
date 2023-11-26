# variant of nameeveryword.py which does not restrict vocabulary to valid word on the list

from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

named_words = []
count = 0

@app.route('/check_word', methods=['POST'])
def check_word():
    global count, named_words
    word = request.json.get('word', '').strip().lower()

    named_words.append(word)
    count += 1

    return jsonify({
        'count': count,
        'last25Words': list(reversed(named_words[-25:])),
        'allWords': sorted(named_words)
    })

if __name__ == '__main__':
    app.run(debug=True)
