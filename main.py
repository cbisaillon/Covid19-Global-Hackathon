import numpy as np
import pandas as pd
from sklearn.utils import shuffle
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

real_data = pd.read_csv('data/True.csv')
fake_data = pd.read_csv('data/Fake.csv')

device = torch.device('cuda')
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased").to(device)

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


def train(train_data, validate_data):
    total_loss = 0
    all_losses = []

    for idx, row in train_data.iterrows():
        try:
            text = str(row['text'])
            splitted_text = text.split(' ')
            try:
                label = torch.tensor([row['is_fake']]).float().to(device)
            except:
                print(torch.tensor([row['is_fake']]).float())

            # text = tokenizer.encode(text, return_tensors="pt")
            # Split the text in parts of 500 characters and run the classification on each part

            parts = []

            text_len = len(text.split(' '))
            delta = 100
            max_parts = 5
            nb_cuts = int(text_len / delta)

            for i in range(nb_cuts + 1):
                text_part = ' '.join(splitted_text[i * delta: (i + 1) * delta])
                parts.append(tokenizer.encode(text_part[:max_parts], return_tensors="pt").to(device))

            optimizer.zero_grad()

            overall_output = torch.zeros((1,2)).to(device)
            try:
                for part in parts:
                    if len(part) > 0:
                        overall_output += model(part.reshape(1, -1))[0]
            except RuntimeError:
                print("GPU out of memory, skipping this entry.")
                continue

            overall_output /= len(parts)

            if label == 0:
                label = torch.tensor([[1.0, 0.0]]).to(device)
            elif label == 1:
                label = torch.tensor([[0.0, 1.0]]).to(device)

            loss = criterion(overall_output, label)
            total_loss += loss.item()
            loss.backward()
            optimizer.step()

            if idx % print_every == 0 and idx > 0:
                average_loss = total_loss / print_every
                print("{}/{}. Average loss: {}".format(idx, len(train_data), average_loss))
                all_losses.append(average_loss)
                total_loss = 0
        except:
            print("Exception occured, skipping entry")

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
