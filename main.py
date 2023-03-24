import requests
from requests.exceptions import HTTPError

import os
from os.path import join
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

import argparse


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
    check_for_redirect(response)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    book_image = soup.find('div', class_='bookimage')
    if book_image:
        book_image = book_image.find('img')['src']
    else:
        book_image = '/images/nopic.gif'

    comments = []
    for comment in soup.find_all('div', class_='texts'):
        comment_text = comment.find('span', class_='black')
        if comment_text:
            comments.append(comment_text.text)

    genres = []
    span_d_book = soup.find('span', class_='d_book')
    if span_d_book:
        for genre in span_d_book.find_all('a'):
            genres.append(genre.text)

    title_parts = soup.find('h1').text.split(':')
    book_title = title_parts[0].strip()
    author = title_parts[2].strip()

    book_data = {
        'title': book_title,
        'author': author,
        'image_url': urljoin('https://tululu.org/', book_image),
        'comments': comments,
        'genres': genres,
    }
    
    return book_data


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


def get_books(ids):
    for book_id in ids:
        url = f'https://tululu.org/txt.php?id={book_id}'
        try:
            book_data = parse_book(book_id)
            book_title = f'{book_id}. {book_data["title"]}'
            download_txt(url, book_title)
            download_image(book_data["image_url"])
            print(book_data["title"])
            print(book_data["author"])
            print(book_data["genres"])
            print()
        except HTTPError:
            print(f'Book with id {book_id}, does not exist')


def main():
    parser = argparse.ArgumentParser(description='Описание что делает программа')
    parser.parse_args()
    parser.add_argument('-s', '--start_id', help='Стартовый id', default=1)
    parser.add_argument('-e', '--end_id', help='Конечный id', default=10)    
    args = parser.parse_args()
    ids = [i for i in range(args.start_id, args.end_id + 1)]
    get_books(ids)


if __name__ == '__main__':
    main()
