import requests
from requests.exceptions import HTTPError
import os
from os.path import join
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def get_book(url, book_title, directory='books'):
    response = requests.get(url)
    check_for_redirect(response)
    response.raise_for_status()
    os.makedirs(directory, exist_ok=True)
    path_to_book = join(BASE_DIR, directory, f'{book_title}.txt')
    
    with open(path_to_book, 'wb') as f:
        f.write(response.content)


def get_books(ids: list[int]):
    for book_id in ids:
        url = f'https://tululu.org/txt.php?id={book_id}'
        try:
            get_book(url, f'{book_id}')
        except HTTPError:
            print('Book with that id, does not exist')


def main():
    ids = [i for i in range(1, 11)]
    get_books(ids)


if __name__ == '__main__':
    main()
