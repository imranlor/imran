from bs4 import BeautifulSoup
import requests

def parsing_akipress():
    url = 'https://akipress.org'

    response = requests.get(url=url)
    print(response)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    all_news = soup.find_all('a', class_='newslink')
    # print(all_news)
    n = 0
    for news in all_news:
        n += 1
        print(f'{n}) {news.text}')
        with open('news.txt', 'a+', encoding='utf-8') as news_file:
            news_file.write(f'{n}) {news.text}\n')
    """Сделайте так чтобы у каждой новости была нумерация и также запишите
    их в txt файл (news.txt)"""

def parsing_sulpak_smartfoniy():
    n = 0
    for i in range(1, 11):
        url = f'https://www.sulpak.kg/f/smartfoniy/osh/?page={i}'

        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'lxml')
        all_phones = soup.find_all('div', class_="product__item-name")
        # print(all_phones)
        for phone in all_phones:
            n += 1
            print(f'{n}) {phone.text}')
parsing_sulpak_smartfoniy()