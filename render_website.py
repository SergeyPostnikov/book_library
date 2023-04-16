import json
import codecs
from livereload import Server
from jinja2 import FileSystemLoader, Environment
from more_itertools import chunked


def get_books(columns):
    with codecs.open('library.json', encoding="utf_8_sig") as f:
        books = json.load(f)
    return books


def on_reload():
    loader = FileSystemLoader('templates')
    env = Environment(loader=loader)

    books = list(chunked(get_books(2)[:-1:], 2))

    template = env.get_template('template.html')
    page = template.render(books=books)
    with open('index.html', 'w', encoding="utf-8") as f:
        f.write(page)


if __name__ == '__main__':
    on_reload()
    server = Server()
    server.watch('templates/template.html', on_reload)
    server.serve(root='.')
