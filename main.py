import requests


def get_logo():
    url = 'https://dvmn.org/assets/img/logo.8d8f24edbb5f.svg'
    response = requests.get(url)
    response.raise_for_status()

    with open('logo.svg', 'wb') as f:
        f.write(response.content)


def get_book(url, book_title):
    response = requests.get(url)
    response.raise_for_status()
    with open(f'{book_title}.txt', 'wb') as f:
        f.write(response.content)


def main():
    get_book(
        'https://tululu.org/txt.php?id=32168', 
        'Пески Марса - Кларк Артур'
        )


if __name__ == '__main__':
    main()
