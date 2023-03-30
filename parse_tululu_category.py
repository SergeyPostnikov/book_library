import requests
from main import BASE_URL, check_for_redirect, get_book
from retry import retry
from requests.exceptions import HTTPError, ConnectionError
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json


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
    all_tables = soup.find_all('table', class_='d_book')
    return all_tables


def parse_book_url(table):
    href = table.find('a')['href']
    book_url = urljoin(BASE_URL, href)
    return book_url


def get_links(amount, digest_number):
    all_tables = []
    urls = []
    for num_page in range(1, amount + 1):
        digest_page = get_digest_page(55, num_page)
        soup = get_soup(digest_page)
        all_tables += get_all_tables(soup)
    
    for table in all_tables:
        book_url = parse_book_url(table)
        urls.append(book_url)
    return urls


def save_book_info(library_list):
    book_json = json.dumps(library_list, ensure_ascii=False)
    with open('library.json', 'w', encoding='utf8') as f:
        f.write(book_json)


def main():
    links = get_links(amount=4, digest_number=55)
    library_list = []
    for link in links:
        try:
            book_id = link.split('b')[1].replace('/', '')
            book_card = get_book(book_id)
            library_list.append(book_card)
        except HTTPError:
            print(f'Book with id {book_id}, does not exist.')
        except ConnectionError:
            print(f'connection lost on book with id: {book_id}.')
    save_book_info(library_list)


if __name__ == '__main__':
    main()
