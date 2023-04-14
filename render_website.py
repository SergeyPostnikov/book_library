from flask import Flask
from flask import render_template
import json
import codecs


app = Flask(__name__)


def get_books():
    with codecs.open('library.json', encoding="utf_8_sig") as f:
        books = json.load(f)
    return books


@app.route("/")
def index():
    books = get_books()
    return render_template('index.html', books=books)


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=9000)
