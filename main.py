import numpy as np
import pandas as pd
from sklearn.utils import shuffle
from transformers import BertTokenizer, BertForSequenceClassification, BertConfig
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import torch.nn.functional as F

real_data = pd.read_csv('data/True.csv')
fake_data = pd.read_csv('data/Fake.csv')

device = torch.device('cuda')
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

model = BertForSequenceClassification.from_pretrained("bert-base-uncased").to(device)
model.config.num_labels = 1

criterion = nn.MSELoss().to(device)
optimizer = optim.SGD(model.parameters(), lr=0.001)

print_every = 300


def prepare_data():
    real_data['is_fake'] = False
    fake_data['is_fake'] = True
    data = pd.concat([real_data, fake_data])

    # Shuffle the data
    data = shuffle(data).reset_index(drop=True)
    return data


def preprocess_text(text):
    parts = []

    text_len = len(text.split(' '))
    delta = 250
    max_parts = 5
    nb_cuts = int(text_len / delta)
    nb_cuts = min(nb_cuts, max_parts)

    for i in range(nb_cuts + 1):
        text_part = ' '.join(text.split(' ')[i * delta: (i + 1) * delta])
        parts.append(tokenizer.encode(text_part, return_tensors="pt", max_length=500).to(device))

    return parts


def train(train_data, validate_data):
    total_loss = 0
    all_losses = []

    for idx, row in train_data.iterrows():
        text_parts = preprocess_text(str(row['text']))
        label = torch.tensor([row['is_fake']]).long().to(device)

        optimizer.zero_grad()

        overall_output = torch.zeros((1, 2)).float().to(device)
        for part in text_parts:
            if len(part) > 0:
                try:
                    input = part.reshape(-1)[:512].reshape(1, -1)
                    # print(input.shape)
                    overall_output += model(input, labels=label)[1].float().to(device)
                except Exception as e:
                    print(str(e))

        #     overall_output /= len(text_parts)
        overall_output = F.softmax(overall_output[0], dim=-1)

        if label == 0:
            label = torch.tensor([1.0, 0.0]).float().to(device)
        elif label == 1:
            label = torch.tensor([0.0, 1.0]).float().to(device)

        # print(overall_output, label)

        print(overall_output, label)

        loss = criterion(overall_output, label)
        total_loss += loss.item()
        loss.backward()
        optimizer.step()

        if idx % print_every == 0 and idx > 0:
            average_loss = total_loss / print_every
            print("{}/{}. Average loss: {}".format(idx, len(train_data), average_loss))
            all_losses.append(average_loss)
            total_loss = 0

    # Save the model
    torch.save(model.state_dict(), "model_after_train.pt")

    plt.plot(all_losses)
    plt.show()


def main():
    data = prepare_data()

    train_data, validate_data, test_data = np.split(data.sample(frac=1), [int(.6 * len(data)), int(.8 * len(data))])

    train_data = train_data.reset_index(drop=True)
    validate_data = validate_data.reset_index(drop=True)
    test_data = test_data.reset_index(drop=True)

    train(train_data, validate_data)


if __name__ == "__main__":
    main()
