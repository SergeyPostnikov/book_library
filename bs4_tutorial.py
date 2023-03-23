import requests
from bs4 import BeautifulSoup


url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

post_title = soup.find('main').find('header').find('h1').text
post_image = soup.find('main').find('img')['src']
post_text = soup.find('div', class_='entry-content').text.strip()

print('Заголовок поста:', post_title)
print('Ссылка на картинку:', post_image)
print('Текст поста:', post_text)
