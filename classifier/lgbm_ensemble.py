import pandas as pd
import lightgbm as lgb
import numpy as np
from imblearn.under_sampling import RandomUnderSampler
import pickle

from sklearn.metrics import recall_score, accuracy_score, confusion_matrix

GRID_PATH = "../data/grid_search_results_top.csv"
N_TOP = 20

class Classifier:
    def __init__(self, classifier, threshold, dataset_remap):
        self.classifier = classifier
        self.threshold = threshold
        self.dataset_remap = dataset_remap

    def predict(self, x):
        return self.classifier.predict(x)

def remove_prob(x):
    res = []
    for i in x:
        i = np.delete(i, 0)
        res.append(i)

    return np.array(res)

def remove_distance(x):
    x = remove_lat_lon(x)
    res = []
    for i in x:
        i = np.delete(i, 3)
        res.append(i)

    return np.array(res)

def remove_lat_lon(x):
    res = []
    for i in x:
        i = np.delete(i, 4)
        i = np.delete(i, 4)
        res.append(i)

    return np.array(res)

# dataset = 0 corresponds to the original dataset
# dataset = 1 corresponds to the dataset without the latitudes and longitudes
# dataset = 2 corresponds to the dataset without the distances

def remap_from_idx(idx):
    match idx:
        case 0:
            return lambda x: x
        case 1:
            return remove_lat_lon
        case 2:
            return remove_distance

class Dataset: 
    def __init__(self, x_train, x_test, x_val, y_train, y_test, y_val):
        self.x_train = x_train
        self.x_test = x_test
        self.x_val = x_val
        self.y_train = y_train
        self.y_test = y_test
        self.y_val = y_val

def classifier_from_params(
    x_train, 
    y_train, 
    num_leaves, 
    num_boost_round
):
    params = {
        "objective": "binary",
        "metric": "binary_logloss",
        "num_leaves": num_leaves,
        "verbosity": 0,
        "is_unbalance": True
    }

    train_data = lgb.Dataset(x_train, label=y_train)
    classifier = lgb.train(params, train_data, num_boost_round=num_boost_round)

    return classifier

# TODO: Introduce the threshold
def evaluate(ensemble, x_test, y_test, threshold=0.5):
    predictions = []
    for classifier in ensemble:
        x_test_ = classifier.dataset_remap(x_test)
        prediction = classifier.predict(x_test_)
        prediction = np.where(prediction > classifier.threshold, 1, 0)
        predictions.append(prediction)

    predictions = np.array(predictions)
    predictions = np.mean(predictions, axis=0)
    predictions = np.where(predictions > threshold, 1, 0)

    matrix = confusion_matrix(y_test, predictions)

    return {
        "accuracy": accuracy_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
        "normalized_precision": normalized_precision(matrix),
        "tn": matrix[0][0],
        "fp": matrix[0][1],
        "fn": matrix[1][0],
        "tp": matrix[1][1]
    }

def normalized_precision(matrix):
    factor = (matrix[1][0] + matrix[1][1]) / (matrix[0][0] + matrix[0][1])
    return matrix[1][1] / (matrix[1][1] + factor * matrix[0][1])

def main():
    top_classifier = pd.read_csv(GRID_PATH).head(N_TOP)
    datasets = pickle.load(open("../data/datasets.pkl", "rb"))
    ensemble = []

    for i, row in top_classifier.iterrows():
        print(f"Iteration: {i}")
        (use_under_sampling, us_strategy) = tuple(row["use_under_sampling"].split(","))
        use_under_sampling = use_under_sampling[1:] == "True"
        us_strategy = float(us_strategy[:-1])

        dataset = datasets[row["dataset"]]
        x_train = dataset.x_train
        y_train = dataset.y_train

        if use_under_sampling:
            us = RandomUnderSampler(sampling_strategy=us_strategy)
            x_train, y_train = us.fit_resample(dataset.x_train, dataset.y_train)

        classifier = classifier_from_params(x_train, y_train, row["num_leaves"], row["num_boost_round"])
        classifier = Classifier(
            classifier, 
            row["threshold"], 
            remap_from_idx(row["dataset"])
        )

        ensemble.append(classifier)

    print(evaluate(ensemble, datasets[0].x_test, datasets[0].y_test))
    print(evaluate(ensemble, datasets[0].x_val, datasets[0].y_val))

if __name__ == "__main__":
    main()
