from chalice import Chalice
import boto3
import json
import requests
import feedparser

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

app = Chalice(app_name='fake-news-api')
endpoint_name = "fake-news-endpoint"


@app.route('/predict', methods=['POST'])
def index():
    # Connect to AWS
    runtime = boto3.Session().client(service_name='sagemaker-runtime', region_name='us-east-2')

    if app.current_request.json_body is None or 'text' not in app.current_request.json_body.keys():
        return "You have to specify the text parameter in the POST request"

    # Send the text to the SageMaker model
    text = json.dumps({
        'text': app.current_request.json_body['text']
    })

    try:
        response = runtime.invoke_endpoint(EndpointName=endpoint_name,
                                           Body=text,
                                           ContentType='application/json',
                                           Accept='Accept')
    except Exception as e:
        return str(e)

    return str(response['Body'].read().decode('utf-8'))


random_user_url = "https://randomuser.me/api/"


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
    feed = feedparser.parse('https://www.who.int/rss-feeds/covid19-news-english.xml')
    # feed = feedparser.parse('https://rss.cbc.ca/lineup/topstories.xml')
    posts = []

    for i in range(per_page):
        post_index = (page * per_page) + i

        if post_index > len(feed.entries) - 1:
            continue

        post = feed.entries[post_index]
        title = post.title
        url = post.link

        text = get_article_from_url(url)

        posts.append({
            'user': users[i],
            'post': {
                'title': title,
                'text': text,
                'link': url
            }
        })

    return posts


def get_article_from_url(url):
    #todo: Faire ca
    return "salut"

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
