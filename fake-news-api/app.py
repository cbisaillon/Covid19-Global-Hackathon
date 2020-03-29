from chalice import Chalice
import boto3
import json
import requests
import feedparser
import random
from goose3 import Goose

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


random_user_url = "https://randomuser.me/api/"

# todo: Find more feeds
feeds = [
    'https://www.who.int/rss-feeds/covid19-news-english.xml',
    'https://rss.nytimes.com/services/xml/rss/nyt/US.xml',
    'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    "https://rss.cbc.ca/lineup/topstories.xml",
    "https://rss.cbc.ca/lineup/canada.xml"
    "https://lifestyle.clickhole.com/rss", # FAKE
    "https://www.theonion.com/rss", # FAKE
    "https://www.thedailymash.co.uk/rss", # FAKE
]


@app.route('/post-list')
def postList():
    page = app.current_request.query_params.get('page')
    per_page = app.current_request.query_params.get('per_page')

    if page is None:
        page = 0
    else:
        page = int(page)

    if per_page is None:
        per_page = 10
    else:
        per_page = int(per_page)

    users = []

    # Randomly generate the users
    for i in range(per_page):
        result = json.loads(requests.get(random_user_url).content)
        first_name = result['results'][0]['name']['first']
        last_name = result['results'][0]['name']['last']
        profile_pic = result['results'][0]['picture']['thumbnail']

        users.append({
            'name': first_name + " " + last_name,
            'profile_pic': profile_pic
        })

    # Get random posts
    posts = []

    for i in range(per_page):
        feed = feedparser.parse(random.choice(feeds))
        post_index = (page * per_page) + i

        if post_index > len(feed.entries) - 1:
            continue

        post = feed.entries[post_index]
        title = post.title
        url = post.link

        text = get_article_from_url(url)

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
        return str(e)

    return str(response['Body'].read().decode('utf-8'))


def get_article_from_url(url):
    response = requests.get(url)
    article_extractor = Goose()
    article = article_extractor.extract(raw_html=response.content)
    text = article.cleaned_text

    text = text.replace('\n', '').encode('ascii', 'ignore').decode('utf-8')
    text = ' '.join(text.replace('\\"', '').split(' ')[:500])

    return text
