from chalice import Chalice
import boto3

app = Chalice(app_name='fake-news-api')
endpoint_name = "fake-news-endpoint-2"
runtime = boto3.Session().client(service_name='sagemaker-runtime', region_name='us-east-2')


@app.route('/predict')
def index():
    text = app.current_request.query_params.get('text')

    try:
        response = runtime.invoke_endpoint(EndpointName=endpoint_name, Body=text, ContentType='string')
    except Exception as e:
        return str(e)
    return {'hello': response}


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
