import boto3
import feedparser
import pymysql
import sys
import requests
from goose3 import Goose
import os
import sys
from dotenv import load_dotenv
load_dotenv()

client = boto3.client('rds')

feeds = [
    'https://www.who.int/rss-feeds/covid19-news-english.xml',
    'https://rss.nytimes.com/services/xml/rss/nyt/US.xml',
    'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    "https://rss.cbc.ca/lineup/topstories.xml",
    "https://www.who.int/rss-feeds/news-english.xml",
    "http://ctvnews.ca/rss/TopStories",
    "http://www.ctvnews.ca/rss/World",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://www.cnbc.com/id/100727362/device/rss/rss.html",
    "https://www.cnbc.com/id/10001147/device/rss/rss.html",
    "https://www.cnbc.com/id/19832390/device/rss/rss.html",
    "https://www.cnbc.com/id/10000113/device/rss/rss.html",
    "https://www.who.int/feeds/entity/emergencies/zika-virus/en/rss.xml",
    "https://www.who.int/feeds/entity/hac/en/rss.xml",
    "http://www.ctvnews.ca/rss/Politics",
    "https://rss.cbc.ca/lineup/canada.xml"
    "https://lifestyle.clickhole.com/rss",  # FAKE
    "https://www.theonion.com/rss",  # FAKE
    "https://www.thedailymash.co.uk/rss",  # FAKE
]

# Connect to the database

try:
    conn = pymysql.connect("fakenews.c1yqjf6isjtg.us-east-2.rds.amazonaws.com", user="admin", db="fake_news",
                           password=os.getenv("DB_PASSWORD"), connect_timeout=5)
except Exception as e:
    print("Error: " + str(e))
    sys.exit()

insert_query = """INSERT INTO news (title, author, url, text) VALUES (%s, %s, %s, %s)"""


def get_article_from_url(url):
    response = requests.get(url)
    article_extractor = Goose()

    article = article_extractor.extract(raw_html=response.content)
    text = article.cleaned_text

    text = text.replace('\n', '').encode('ascii', 'ignore').decode('utf-8')
    text = ' '.join(text.replace('\\"', '').split(' ')[:])

    return text


for feedUrl in feeds:
    feed = feedparser.parse(feedUrl)
    print(feedUrl + " " + str(len(feed.entries)))
    for post in feed.entries:
        title = post.title
        url = post.link
        text = get_article_from_url(url)

        if len(text.split(' ')) > 200:
            # Add to the database if title doesnt exists
            cursor = conn.cursor()
            try:
                cursor.execute(insert_query, (title, "author", url, text))
            except pymysql.err.IntegrityError as e:
                print("Title alread present")

conn.commit()
