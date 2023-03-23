import requests
from requests.exceptions import HTTPError
import os
from os.path import join
from pathlib import Path

from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def parse_book(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    book_title = (
        soup.find('h1')
        .text
        .replace('\xa0', '')
        .replace(':', '')
        )
    # book_image = soup.find('div', class_='bookimage').find('img')['src']
    return book_title 


def save_book(url, book_title, directory='books'):
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
            book_title = parse_book(book_id)
            save_book(url, book_title)
        except HTTPError:
            print('Book with id {book_id}, does not exist')


def main():
    ids = [i for i in range(1, 11)]
    get_books(ids)
    # print(parse_book(32169))


if __name__ == '__main__':
    main()
