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
        raise requests.exceptions.HTTPError('URL has been redirected')


def get_book_title(soup):
    title_parts = soup.find('h1').text.split(':')
    return title_parts[0].strip()


def get_author(soup):
    title_parts = soup.find('h1').text.split(':')
    return title_parts[2].strip()


def get_book_image(url, soup):
    book_image = soup.find('div', class_='bookimage')
    if book_image:
        book_image = urljoin(url, book_image.find('img')['src'])
    else:
        book_image = '/images/nopic.gif'
    return book_image


def get_comments(soup):
    comments = []
    for comment in soup.find_all('div', class_='texts'):
        comment_text = comment.find('span', class_='black')
        if comment_text:
            comments.append(comment_text.text)
    return comments


def get_genres(soup):
    genres = []
    span_d_book = soup.find('span', class_='d_book')
    if span_d_book:
        for genre in span_d_book.find_all('a'):
            genres.append(genre.text)
    return genres


def parse_book(book_id):
    base_url = 'https://tululu.org/'
    url = urljoin(base_url, f'b{book_id}/')
    response = requests.get(url)
    check_for_redirect(response)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    book_data = {
        'title': get_book_title(soup),
        'author': get_author(soup),
        'image_url': get_book_image(url, soup),
        'comments': get_comments(soup),
        'genres': get_genres(soup),
    }
    
    return book_data


def download_txt(book_id, filename, folder='books/'):
    payload = {'id': 'book_id'}
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


def get_book(book_id):
    try:
        book_info = parse_book(book_id)
        book_title = f'{book_id}. {book_info["title"]}'
        download_txt(book_id, book_title)
        download_image(book_info["image_url"])
        print(book_info["title"])
        print(book_info["author"])
        print(book_info["genres"])
        print()
    except HTTPError:
        print(f'Book with id {book_id}, does not exist')


def main():
    parser = argparse.ArgumentParser(description='')

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
        get_book(book_id)


if __name__ == '__main__':
    main()
