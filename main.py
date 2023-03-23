import requests
from requests.exceptions import HTTPError

import os
from os.path import join
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

BASE_DIR = Path(__file__).resolve().parent


def get_filename(url):
    path = urlparse(url).path
    row_name = path.split("/")[-1]
    filename = unquote(row_name)
    return filename


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def parse_book(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    try:
        book_image = soup.find('div', class_='bookimage').find('img')['src']
    except AttributeError:
        book_image = '/images/nopic.gif'

    try:
        div_texts = soup.find_all('div', class_='texts')
        comments = [comment.find('span', class_='black').text for comment in div_texts]
    except AttributeError:
        comments = []

    book_title, *args = soup.find('h1').text.split(':')

    return book_title.strip(), urljoin('https://tululu.org/', book_image), comments


def download_txt(url, filename, folder='books/'):

    response = requests.get(url)
    check_for_redirect(response)
    response.raise_for_status()

    validated_filename = sanitize_filename(filename)
    
    os.makedirs(folder, exist_ok=True)
    filepath = join(folder, f'{validated_filename}.txt')
    
    with open(filepath, 'wb') as f:
        f.write(response.content)
    return filepath


def download_image(url, folder='images/'):

    filename = get_filename(url)
    response = requests.get(url)
    check_for_redirect(response)
    response.raise_for_status()

    validated_filename = sanitize_filename(filename)
    
    os.makedirs(folder, exist_ok=True)
    filepath = join(folder, f'{validated_filename}.jpg')
    
    with open(filepath, 'wb') as f:
        f.write(response.content)
    return filepath


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
            title, image_url, comments = parse_book(book_id)
            book_title = f'{book_id}. {title}'
            # download_txt(url, book_title)
            # download_image(image_url)
            print(comments)
        except HTTPError:
            print(f'Book with id {book_id}, does not exist')


def main():
    ids = [i for i in range(1, 11)]
    get_books(ids)


if __name__ == '__main__':
    main()
