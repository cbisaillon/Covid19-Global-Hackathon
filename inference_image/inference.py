from flask import Flask
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import torch.nn.functional as F
from flask import request
import boto3
import tarfile
import subprocess
import os
import multiprocessing
import signal
import sys
import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

app = Flask(__name__)
model_file = "/opt/ml/model/model_after_train.pt"

device = torch.device('cpu')

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased").to(device)
model.load_state_dict(torch.load(model_file, map_location=torch.device('cpu')))
model.config.num_labels = 1


def preprocess_text(text):
    parts = []

    text_len = len(text.split(' '))
    delta = 300
    max_parts = 5
    nb_cuts = int(text_len / delta)
    nb_cuts = min(nb_cuts, max_parts)

    for i in range(nb_cuts + 1):
        text_part = ' '.join(text.split(' ')[i * delta: (i + 1) * delta])
        # remove stop words
        # text_part = text_part.replace("\n", "")
        # text_part = text_part.lower()
        # text_part = " ".join([w for w in text_part.split(' ') if not w in stop_words])

        parts.append(tokenizer.encode(text_part, return_tensors="pt", max_length=500).to(device))

    return parts


@app.route('/invocations', methods=['POST'])
def inference():
    texts = request.json['text']

    results = []

    for text in texts:
        text_parts = preprocess_text(text)
        overall_output = torch.zeros((1, 2)).to(device)
        try:
            for part in text_parts:
                if len(part) > 0:
                    overall_output += model(part.reshape(1, -1))[0]
        except RuntimeError:
            print("GPU out of memory, skipping this entry.")

        overall_output = F.softmax(overall_output[0], dim=-1)

        value, result = overall_output.max(0)

        a = {
            'result': result.item(),
            'chance': value.item()
        }

        if a['chance'] < 0.9 and a['result'] == 1:
            chance = 1.0 - a['chance']
            result = 0

            results.append({
                'result': result,
                'chance': chance
            })
        else:
            results.append(a)



    return {
        'results': results
    }


@app.route('/ping', methods=['GET'])
def ping():
    return "YES"


cpu_count = multiprocessing.cpu_count()

model_server_timeout = os.environ.get('MODEL_SERVER_TIMEOUT', 60)
model_server_workers = int(os.environ.get('MODEL_SERVER_WORKERS', cpu_count))


def sigterm_handler(nginx_pid, gunicorn_pid):
    try:
        os.kill(nginx_pid, signal.SIGQUIT)
    except OSError:
        pass
    try:
        os.kill(gunicorn_pid, signal.SIGTERM)
    except OSError:
        pass

    sys.exit(0)


def start_server():
    print('Starting the inference server with {} workers.'.format(model_server_workers))

    # link the log streams to stdout/err so they will be logged to the container logs
    subprocess.check_call(['ln', '-sf', '/dev/stdout', '/var/log/nginx/access.log'])
    subprocess.check_call(['ln', '-sf', '/dev/stderr', '/var/log/nginx/error.log'])

    nginx = subprocess.Popen(['nginx', '-c', '/opt/program/nginx.conf'])
    gunicorn = subprocess.Popen(['gunicorn',
                                 '--timeout', str(model_server_timeout),
                                 '-k', 'gevent',
                                 '-b', 'unix:/tmp/gunicorn.sock',
                                 '-w', str(model_server_workers),
                                 'wsgi:app'])

    signal.signal(signal.SIGTERM, lambda a, b: sigterm_handler(nginx.pid, gunicorn.pid))

    # If either subprocess exits, so do we.
    pids = set([nginx.pid, gunicorn.pid])
    while True:
        pid, _ = os.wait()
        if pid in pids:
            break

    sigterm_handler(nginx.pid, gunicorn.pid)
    print('Inference server exiting')


if __name__ == '__main__':
    start_server()

# app.run(debug=False, port=8080)
