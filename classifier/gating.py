import numpy as np
import pandas as pd
import lightgbm
import torch
import json
from differential_evolution import binary_cross_entropy
# from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score

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
    train_dataset = data()
    print(train_dataset[1].sum())
    test_dataset = data("../data/test.csv")
    print("got datasets")
    models = load_models(train_dataset)
    print("loaded models")
    x_test, y_test = test_dataset

    # for model in models:
    #     y_pred = model.predict(x_test)
    #     y_pred = np.round(y_pred)
    #     print("Acc:", accuracy_score(y_test, y_pred))
    #     print("Matrix:", confusion_matrix(y_test, y_pred))
    #     print("Recall:", recall_score(y_test, y_pred))
    #     print("BCE:", binary_cross_entropy(y_test, y_pred))

    # predictions = np.array([model.predict(x_test) for model in models])
    # predictions = predictions.transpose()
    # y_pred = []
    # for pred in predictions:
    #     pred = np.round(np.mean(pred))
    #     y_pred.append(pred)
    # y_pred = np.array(y_pred)

    # print(accuracy_score(y_test, y_pred))
    # print(confusion_matrix(y_test, y_pred))
    # print(recall_score(y_test, y_pred))
    # print(binary_cross_entropy(y_test, y_pred))


    x_train, y_train = make_data(models, train_dataset)
    x_test, y_test = make_data(models, test_dataset)

    print("created data")

    # we trained the models already on the training data, thus it is questionable whether we 
    # we can train the gating model based on the predictions made on the training data by the models
    # we might have to split the test set as well and use one part of it as the training set for the
    # gating model.

    gating_model = GatingNetwork(len(x_train[0]), len(models))

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

    x_test, y_test = test_dataset
    predictions = np.array([model.predict(x_test) for model in models])
    predictions = predictions.transpose()
    xs = torch.tensor(predictions, dtype=torch.float32)
    routes = gating_model(xs).detach().numpy()

    y_pred = []
    for i, route in enumerate(routes):
        best = np.argsort(route)[-2:]
        best_predictions = [predictions[i, j] for j in best]
        prediction = np.round(np.mean(best_predictions))
        y_pred.append(prediction)

    print(accuracy_score(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    print(recall_score(y_test, y_pred))




def data(path="../data/train.csv") -> tuple[np.ndarray, np.ndarray]:
    data = pd.read_csv(path)
    ys = data["is_damaged"].values
    xs = data["vec_repr"].apply(lambda x: json.loads(x))
    xs = np.array(xs.tolist())

    return xs, ys

def make_data(models, data):
    print("making data")
    xs, ys = data
    predictions = np.array([model.predict(xs) for model in models])
    predictions = predictions.transpose()

    out = []
    for predicted, actual in zip(predictions, ys):
        predicted = np.array(predicted)
        diff = np.abs(predicted - actual)
        best = np.argsort(diff)[:2]
        out.append([1 if i in best else 0 for i in range(len(models))])

    return predictions, out
        

def lgbm_model_from_obj(obj, xs, ys):
    print("training model")
    params = {
        "is_unbalance": True,
        "objective": "binary",
        "metric": "binary_logloss",
        "verbosity": -1,
        "num_leaves": obj["num_leaves"],
        "max_depth": obj["max_depth"],
        "min_data_in_leaf": obj["min_data_in_leaf"],
        "learning_rate": obj["learning_rate"],
    }

    dataset = lightgbm.Dataset(xs, label=ys)
    model = lightgbm.train(params, dataset)
    return model

def load_models(train_dataset, path="./models/models.json"):
    xs, ys = train_dataset
    with open(path, "r") as f:
        arr = json.load(f)
        models = [lgbm_model_from_obj(obj, xs, ys) for obj in arr]
        return models


if __name__ == "__main__":
    main()
