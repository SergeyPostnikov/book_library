import argparse
import json

from os.path import join
from urllib.parse import urljoin

import requests

from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from retry import retry

from parse_tululu_by_id import BASE_DIR
from parse_tululu_by_id import BASE_URL
from parse_tululu_by_id import check_for_redirect
from parse_tululu_by_id import get_book


@retry(ConnectionError, tries=3, delay=10)
def get_digest_page(digest_num, page_number=1):
    digest_url = urljoin(BASE_URL, f'/l{digest_num}/')
    url = urljoin(digest_url, f'{page_number}')
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    return response


def get_soup(response):
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_all_tables(soup):
    selector = 'table.d_book'
    all_tables = soup.select(selector)
    return all_tables


def parse_book_url(table):
    href = table.select_one('a')['href']
    book_url = urljoin(BASE_URL, href)
    return book_url


def get_links(start_page, end_page,digest_number):
    all_tables = []
    urls = []
    for num_page in range(start_page, end_page + 1):
        digest_page = get_digest_page(55, num_page)
        soup = get_soup(digest_page)
        all_tables += get_all_tables(soup)
    
    for table in all_tables:
        book_url = parse_book_url(table)
        urls.append(book_url)
    return urls


def save_book_info(library_list, folder):
    book_json = json.dumps(library_list, ensure_ascii=False)
    path_to_json = join(BASE_DIR, folder, 'library.json')
    with open(path_to_json, 'w', encoding='utf8') as f:
        f.write(book_json)


def get_argument_parser():
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
            type=bool, 
            help='Skip downloading title image of books',
            default=False)

    parser.add_argument(
            '--skip_txt', 
            type=bool, 
            help='Skip downloading text of books',
            default=False) 

    parser.add_argument(
            '--json_path', 
            help='Folder for storing library.json ',
            default=BASE_DIR)     
    args = parser.parse_args()
    return args


def main():
    args = get_argument_parser()
    links = get_links(args.start_page, args.end_page, digest_number=55)
    library_list = []
    for link in links:
        try:
            book_id = link.split('b')[1].replace('/', '')
            book_card = get_book(book_id, args.dest_folder, args.skip_txt, args.skip_imgs,)
            library_list.append(book_card)
        except HTTPError:  
            print(f'Book with id {book_id}, does not exist.')
        except ConnectionError:
            print(f'connection lost on book with id: {book_id}.')
    save_book_info(library_list, '')


if __name__ == '__main__':
    main()
