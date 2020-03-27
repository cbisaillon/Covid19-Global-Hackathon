# This script scrape the website politifact.com to
# retrieve verified real news relating corona virus and verified fake news
import requests
from bs4 import BeautifulSoup
import sqlite3
import string

rulings = {
    'true': 'true',
    'mostlytrue': 'mostly-true',
    'halftrue': 'half-true',
    'fake': 'false',
    'reallyfake': 'pants-fire',
}

base_url = "https://www.politifact.com"
main_url = "https://www.politifact.com/factchecks/list/?category=coronavirus&ruling={ruling}"

database = sqlite3.connect('corona-data.db')


def configure_database():
    cursor = database.cursor()
    create_table = "CREATE TABLE IF NOT EXISTS dataset (id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                   "title TEXT NOT NULL UNIQUE, " \
                   "texte TEXT NOT NULL," \
                   "ruling TEXT NOT NULL)"

    cursor.execute(create_table)
    cursor.close()


import json


def add_entry_to_database(title, text, ruling):
    cursor = database.cursor()
    query = 'INSERT INTO dataset (title, texte, ruling) VALUES ("%s", "%s", "%s")' % (title, text, ruling)

    cursor.execute(query)
    database.commit()
    cursor.close()


def clean():
    database.close()


def filter_text(text):
    return "".join(filter(lambda x: x in string.printable, text)).strip().replace('"','')


def get_article(article_url):
    print(article_url)
    page = requests.get(article_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    article = soup.find('article', class_="m-textblock").find_all('p')
    text = " ".join(
        [paragraph.get_text() for paragraph in article[:-1]])  # Remove the last paragraph that say "We rate this true"

    text = filter_text(text)
    return text


def create_dataset():
    for key, ruling in rulings.items():
        ruling_url = main_url.replace('{ruling}', ruling)
        page = requests.get(ruling_url)

        if page.status_code == 200:
            print(ruling_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            title_divs = soup.find_all(class_='m-statement__quote')
            for title_div in title_divs:
                articles = {}
                link = list(title_div.children)[1]
                title = filter_text(link.get_text())
                article_url = link['href']

                text = get_article(base_url + article_url)
                add_entry_to_database(title, text, ruling)

        else:
            print("Error while retrieving url: {}".format(ruling_url))


if __name__ == "__main__":
    configure_database()
    create_dataset()
    clean()
