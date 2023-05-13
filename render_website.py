import argparse
import codecs
import json
import os
from os.path import join

from jinja2 import Environment
from jinja2 import FileSystemLoader
from livereload import Server
from more_itertools import chunked

from parse_tululu_by_id import BASE_DIR


def prepare_pages(per_page: int, per_row: int, library_file: str) -> list:
    with codecs.open(library_file, encoding="utf_8_sig") as f:
        books = json.load(f)
    columns = [i for i in chunked(books, per_row)]
    chunk = chunked(columns, per_page // per_row)
    book_pages = [page for page in chunk]

    return book_pages


def render_template(page_number, books, template='template.html'):
    rout = join(BASE_DIR, 'books', f'index{page_number}.html')
    serialized_page = {
        'books': books,
        'number': page_number,
    }
    rendered_page = template.render(page=serialized_page)
    with open(rout, 'w', encoding="utf-8") as f:
        f.write(rendered_page)


def on_reload(folder='pages', library_file='library.json'):
    os.makedirs(folder, exist_ok=True)
    loader = FileSystemLoader('templates')
    env = Environment(loader=loader)
    template = env.get_template('template.html')
    books_pages = prepare_pages(
        per_page=8, 
        per_row=2, 
        library_file=library_file)
    page_number = 1

    page_nums = [i for i in range(1, len(books_pages) + 1)]

    for page in books_pages:
        rout = join(BASE_DIR, folder, f'index{page_number}.html')

        serialized_page = {
            'books': page,
            'number': page_number,
            'ids': page_nums
        }

        rendered_page = template.render(page=serialized_page)

        with open(rout, 'w', encoding="utf-8") as f:
            f.write(rendered_page)
        page_number += 1


def get_arguments():
    parser = argparse.ArgumentParser(
        prog='library parser',
        description='A script to download books and their covers from tululu.org',
        epilog='usage: parse_tululu_category.py [--start_page START_ID] [--end_page END_ID]'
        )

    parser.add_argument(
        '--json_path', 
        help='Path where library.json placed',
        default='library.json')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_arguments()
    on_reload(library_file=args.json_path)
    server = Server()
    server.watch('templates/template.html', on_reload)
    server.serve(root='.')
