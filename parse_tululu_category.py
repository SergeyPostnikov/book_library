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


def get_book_id(soup):
    book_id = soup.find_all('a', attrs={'title': 'Бесплатная библиотека'})
    return book_id


def parse_book_card(digest_page):
    soup = BeautifulSoup(digest_page.text, 'lxml')
    book_id = get_book_id(soup)
    book_card = {
        'book_id': book_id
    }
    return book_card


if __name__ == '__main__':
    digest_page = get_digest_page(55)
    # print(digest_page.text)
    book_card = parse_book_card(digest_page)
    print(book_card)