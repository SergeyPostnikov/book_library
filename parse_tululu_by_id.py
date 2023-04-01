import requests

from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

import os
import time

from os.path import join
from pathlib import Path
from urllib.parse import unquote
from urllib.parse import urljoin
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

import argparse


BASE_DIR = Path(__file__).resolve().parent
BASE_URL = 'https://tululu.org/'

TRIES = 1
DELAY = 1
MAX_DELAY = 1


def get_filename(url):
    path = urlparse(url).path
    row_name = path.split("/")[-1]
    filename = unquote(row_name)
    return filename


def check_for_redirect(response):
    if response.history:
        raise HTTPError('URL has been redirected')


def get_book_title(soup):
    title_parts = soup.select_one('h1').text.split(':')
    book_name = title_parts[0].strip()
    book_author = title_parts[2].strip()
    return book_name, book_author


def get_book_image(soup):
    selector = 'div.bookimage img'
    book_image = soup.select_one(selector)
    if book_image:
        book_image = urljoin(BASE_URL, book_image['src'])
    else:
        book_image = urljoin(BASE_URL, '/images/nopic.gif')
    return book_image


def get_comments(soup):
    comments = []
    for comment in soup.select('div.texts'):
        comment_text = comment.select_one('span.black')
        if comment_text:
            comments.append(comment_text.text)
    return comments


def get_genres(soup):
    genres = []
    span_d_book = soup.select_one('span.d_book')
    if span_d_book:
        for genre in span_d_book.select('a'):
            genres.append(genre.text)
    return genres


def get_page(url):
    response = requests.get(url)
    check_for_redirect(response)
    response.raise_for_status()
    return response


def parse_book(response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_name, book_author = get_book_title(soup)
    book_page = {
        'title': book_name,
        'author': book_author,
        'image_url': get_book_image(soup),
        'comments': get_comments(soup),
        'genres': get_genres(soup),
    }
    
    return book_page


def download_txt(book_id, filename, folder='books/'):
    payload = {'id': book_id}
    url = 'https://tululu.org/txt.php'
    response = requests.get(url, params=payload)
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


def get_book(book_id, folder='books', skip_txt=False, skip_imgs=False):
    url = urljoin(BASE_URL, f'b{book_id}/')
    row_page = get_page(url)
    book_page = parse_book(row_page)
    book_title = f'{book_id}. {book_page["title"]}'
    if not skip_txt:
        book_path = download_txt(book_id, book_title, folder)
        book_page['book_path'] = book_path
    if not skip_imgs:
        image_src = download_image(book_page["image_url"])
        book_page['image_src'] = image_src
    return book_page


def main():
    parser = argparse.ArgumentParser(
        prog='library parser',
        description='A script to download books and their covers from tululu.org',
        epilog='usage: parse_tululu_by_id [--start_id START_ID] [--end_id END_ID]'
        )

    parser.add_argument(
            '--start_id', 
            type=int, 
            help='an integer for the starting id',
            default=1
        )
    parser.add_argument(
            '--end_id', 
            type=int, 
            help='an integer for the ending id',
            default=10)   
    
    args = parser.parse_args()
    for book_id in range(args.start_id, args.end_id + 1):
        try:
            get_book(book_id)
        except HTTPError:
            print(f'Book with id {book_id}, does not exist.')
        except ConnectionError:
            print(f'connection lost on book with id: {book_id}.')
            time.sleep(1)
            continue


if __name__ == '__main__':
    main()
