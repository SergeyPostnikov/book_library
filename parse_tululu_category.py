import requests
from main import BASE_URL, check_for_redirect
from retry import retry
from requests.exceptions import ConnectionError
from urllib.parse import urljoin
from bs4 import BeautifulSoup


@retry(ConnectionError, tries=3, delay=10)
def get_digest_page(digest_num):
    url = urljoin(BASE_URL, f'/l{digest_num}/')
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    return response


def get_soup(response):
    soup = BeautifulSoup(digest_page.text, 'lxml')
    return soup


def get_all_tables(soup):
    all_tables = soup.find_all('table', class_='d_book')
    return all_tables


def parse_book_card(table):
    href = table.find('a')['href']
    download_url = urljoin(BASE_URL, href)
    book_card = {
        'download_url': download_url
    }
    return book_card


if __name__ == '__main__':
    from pprint import pprint
    digest_page = get_digest_page(55)
    soup = get_soup(digest_page)
    all_tables = get_all_tables(soup)
    for table in all_tables[:25]:
        book_card = parse_book_card(table)
        pprint(book_card['download_url'])
