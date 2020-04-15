# Covid19 Global Hackathon
For the Covid19 Global Hackathon, we worked on a machine learning algorithm able to classify fake and real news.
Given the text of an article, our algorithm is able to predict if it is considered fake or real and at what percentage.
We built a small neural network where each of the posts pass through our algorithm to show how easily it could be integrated to existing social networks. We also developed a browser extension that parse the text of the articles that you are reading through our network and tell the user to be carefull when it gesses that it is fake.

## Installation
1. Create a new conda environment: `conda env create -n fakenews`
1. Enter the environment: `activate fakenews` (windows). `conda activate fakenews` (Unix)
1. Install the dependencies: `pip install -r requirements.txt`

## Training the model
To train the model yourself, run the main.py file.

## Creating the Chalice endpoint
To create the chalice endpoint make sure that your have AWS cli installed

1. Configure AWS cli if not already done: `aws configure`
1. cd into the `fake-news-api` directory
1. Install the dependencies: `pip install -r requirements.txt`
1. Run the command: `chalice deploy`

## Creating the SageMaker endpoint
The inference image is created from the `inference_image` directory.
To create the SageMaker endpoint:

1. create a docker image of this repository and upload the container to AWS ECR.
1. In the SageMaker dashboard, create a new model by specifiying the uploaded container.
1. Also in the SageMaker dashboard, create an endpoint from the previously created model.
