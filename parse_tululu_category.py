import argparse
import json
import time

from os.path import join
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

from parse_tululu_by_id import BASE_DIR
from parse_tululu_by_id import BASE_URL
from parse_tululu_by_id import get_book
from parse_tululu_by_id import get_page


def get_book_cards(response):
    soup = BeautifulSoup(response.text, 'lxml')
    selector = 'table.d_book'
    book_cards = soup.select(selector)
    return book_cards


def parse_book_url(table):
    href = table.select_one('a')['href']
    book_url = urljoin(BASE_URL, href)
    return book_url
 

def get_links(start_page, end_page, digest_number):
    book_cards = []
    urls = []
    for page_number in range(start_page, end_page + 1):
        digest_url = urljoin(BASE_URL, f'/l{digest_number}/')
        url = urljoin(digest_url, f'{page_number}')
        digest_page = get_page(url)
        book_cards += get_book_cards(digest_page)
    
    for table in book_cards:
        book_url = parse_book_url(table)
        urls.append(book_url)
    return urls


def save_catalog(library_catalog, folder):
    path_to_json = join(BASE_DIR, folder, 'library.json')
    with open(path_to_json, 'w', encoding='utf8') as file:
        json.dump(library_catalog, file, ensure_ascii=False)


def get_arguments():
    parser = argparse.ArgumentParser(
        prog='library parser',
        description='A script to download books and their covers from tululu.org',
        epilog='usage: parse_tululu_category.py [--start_page START_ID] [--end_page END_ID]'
        )

    parser.add_argument(
            '--start_page', 
            type=int, 
            help='Nubmer of page for the start parsing',
            default=1
        )
    parser.add_argument(
            '--end_page', 
            type=int, 
            help='Nubmer of page for the stop parsing',
            default=1) 

    parser.add_argument(
            '--dest_folder', 
            help='Folder for storing txt files of books',
            default=join(BASE_DIR, 'books')) 

    parser.add_argument(
            '--skip_imgs', 
            help='Skip downloading title image of books',
            action='store_true'
            )

    parser.add_argument(
            '--skip_txt', 
            help='Skip downloading text of books',
            action='store_true'
            ) 

    parser.add_argument(
            '--json_path', 
            help='Folder for storing library.json ',
            default=BASE_DIR)     
    args = parser.parse_args()
    return args


def main():
    args = get_arguments()
    links = get_links(args.start_page, args.end_page, digest_number=55)
    library_catalog = []
    for link in links:
        try:
            book_id = link.split('b')[1].replace('/', '')
            book_card = get_book(book_id, args.dest_folder, args.skip_txt, args.skip_imgs,)
            library_catalog.append(book_card)
        except HTTPError:  
            print(f'Book with id {book_id}, does not exist.')
        except ConnectionError:
            print(f'connection lost on book with id: {book_id}.')
            time.sleep(1)
            continue
    save_catalog(library_catalog, args.json_path)


if __name__ == '__main__':
    main()
