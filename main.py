import requests
from bs4 import BeautifulSoup

KEYWORDS = {'дизайн', 'фото', 'web', 'python'}
URL = 'https://habr.com'


def get_articles():
    ret = requests.get('https://habr.com/ru/all/')
    soup = BeautifulSoup(ret.text, features='html.parser')
    return soup.find_all('article')


def get_words(article):
    preview = article.find(class_="tm-article-snippet")
    if preview:
        return {word.lower() for word in preview.text.split()}
    else:
        return {}


def get_link(article):
    return URL + article.find('h2').find('a').attrs.get('href')


def get_date(article):
    return article.find('time').attrs.get('title').split(',')[0]


def get_title(article):
    return article.find('h2').find('span').text


def scan():
    out = []
    articles = get_articles()
    for article in articles:
        preview = get_words(article)
        if preview & KEYWORDS:
            date = get_date(article)
            title = get_title(article)
            link = get_link(article)
            out.append(f"{date} - {title} - {link}")
    return out


print(scan())
