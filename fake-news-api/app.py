from chalice import Chalice
import boto3
import json
import requests
import feedparser
import random
from goose3 import Goose
import pymysql
import os
import sys
from dotenv import load_dotenv

load_dotenv()

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

app = Chalice(app_name='fake-news-api')
endpoint_name = "fake-news-endpoint"
runtime = boto3.Session().client(service_name='sagemaker-runtime', region_name='us-east-2')


@app.route('/predict', methods=['POST'])
def index():
    # Connect to AWS
    if app.current_request.json_body is None or 'text' not in app.current_request.json_body.keys():
        return "You have to specify the text parameter in the POST request"

    return queryModel(app.current_request.json_body['text'])


@app.route('/post-list')
def postList():
    per_page = app.current_request.query_params.get('per_page')

    if per_page is None:
        per_page = 10
    else:
        per_page = int(per_page)

    users = []

    # Randomly generate the users
    random_user_url = "https://randomuser.me/api/?results=%s" % (per_page)
    result = json.loads(requests.get(random_user_url).content)
    for user in result['results']:
        first_name = user['name']['first']
        last_name = user['name']['last']
        profile_pic = user['picture']['thumbnail']

        users.append({
            'name': first_name + " " + last_name,
            'profile_pic': profile_pic
        })

    # Get random posts
    posts = []

    # Connect to database
    try:
        conn = pymysql.connect("fakenews.c1yqjf6isjtg.us-east-2.rds.amazonaws.com", user="admin", db="fake_news",
                               password=os.getenv("DB_PASSWORD"), connect_timeout=5)
    except Exception as e:
        print("Error: " + str(e))

    query = """SELECT title,url,text FROM news ORDER BY RAND() LIMIT %s"""
    cursor = conn.cursor()
    cursor.execute(query % (per_page))
    news = cursor.fetchall()

    for i, new in enumerate(news):
        title = new[0]
        url = new[1]
        text = new[2]

        model_prediction = json.loads(queryModel(text))

        posts.append({
            'user': users[i],
            'post': {
                'title': title,
                'text': text,
                'link': url
            },
            'is_fake': model_prediction['result'],
            'chance': model_prediction['chance'],
        })

    return posts

@app.route('/predict-url')
def predictUrl():
    url = app.current_request.query_params.get('url')
    try:
        text = get_article_from_url(url)
    except Exception as e:
        return json.dumps({"error": str(e)})

    return queryModel(text)


def queryModel(text):
    # Send the text to the SageMaker model
    text = json.dumps({
        'text': text
    })

    try:
        response = runtime.invoke_endpoint(EndpointName=endpoint_name,
                                           Body=text,
                                           ContentType='application/json',
                                           Accept='Accept')
    except Exception as e:
        pass
    return str(response['Body'].read().decode('utf-8'))


def get_article_from_url(url):
    response = requests.get(url)
    article_extractor = Goose()
    try:
        article = article_extractor.extract(raw_html=response.content)
        text = article.cleaned_text

        text = text.replace('\n', '').encode('ascii', 'ignore').decode('utf-8')
        text = ' '.join(text.replace('\\"', '').split(' ')[:])

        if len(text.split(' ')) < 200:
            raise Exception("Not enough words in the article")
    except UnicodeDecodeError:
        raise Exception("Cant find a valid article on this web page")

    return text
