import numpy as np
import pandas as pd
from os import listdir
import pickle
import torch
import json
from sklearn.model_selection import train_test_split

class GatingNetwork(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super(GatingNetwork, self).__init__()
        self.fc1 = torch.nn.Linear(input_size, 128)
        self.fc2 = torch.nn.Linear(128, 64)
        self.fc3 = torch.nn.Linear(64, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))
        return x

def main():
    mods = models()
    train_dataset = data()
    test_dataset = data("../data/test.csv")

    x_train, y_train = make_data(mods, train_dataset)
    x_test, y_test = make_data(mods, test_dataset)
    gating_model = GatingNetwork(train_dataset.columns.size - 1, len(mods))

    criterion = torch.nn.BCELoss()
    optimizer = torch.optim.Adam(gating_model.parameters(), lr=0.01)
    for epoch in range(100):
        inputs = torch.tensor(x_train, dtype=torch.float32)
        labels = torch.tensor(y_train, dtype=torch.float32)
        optimizer.zero_grad()
        outputs = gating_model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch} loss: {loss.item()}")

    torch.save(gating_model, "./gating_model.pt")

    inputs = torch.tensor(x_test, dtype=torch.float32)
    labels = torch.tensor(y_test, dtype=torch.float32)
    outputs = gating_model(inputs)
    loss = criterion(outputs, labels)
    print(f"Test loss: {loss.item()}")


def data(path="../data/train.csv") -> tuple[np.ndarray, np.ndarray]:
    data = pd.read_csv(path)
    ys = data["is_damaged"].values
    xs = data["vec_repr"].apply(lambda x: json.loads(x))
    xs = np.array(xs.tolist())

    return xs, ys

def make_data(models, data):
    xs, ys = data
    predictions = []
    for x in xs:
        prediction = [model.predict([x])[0] for model in models]
        predictions.append(prediction)

    out = []
    for predicted, actual in zip(predictions, ys):
        predicted = np.array(predicted)
        diff = np.abs(predicted - actual)
        best = np.argsort(diff)[:2]
        out.append([1 if i in best else 0 for i in range(len(models))])

    return xs, out
        

def models(path="./models"):
    models = []
    for file in listdir(path):
        with open(f"{path}/{file}", "rb") as f:
            model = pickle.load(f)
            models.append(model)
    return models


if __name__ == "__main__":
    main()
