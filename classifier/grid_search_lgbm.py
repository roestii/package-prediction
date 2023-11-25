import lightgbm
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

def main():
    model_path = "./models/lgbm_t05_n250_wdal.pkl"
    #dataset_path = "../data/with_cutted/leftover.jsonl"
    dataset_path = "../data/dataset_distance_and_locations.jsonl"
    #validation_path = "../data/with_cutted/cutted.jsonl"

    (x, y) = dataset(dataset_path)
    #(x_val, y_val) = dataset(validation_path)
    (x_train, x_test, y_train, y_test) = train_test_split(x, y, shuffle=True, test_size=0.2)
    (x_train, x_val, y_train, y_val) = train_test_split(x_train, y_train, shuffle=True, test_size=0.2)

    #smote = SMOTE(random_state=42, sampling_strategy=0.1)
    #under_sampler = RandomUnderSampler(random_state=42)
    #x_train, y_train = smote.fit_resample(x_train, y_train) 
    #x_train, y_train = under_sampler.fit_resample(x_train, y_train)

    #weights = {
    #    0: 1,
    #    1: 100,
    #}

    #setting the according parameteres for the LightGBM classifier
    #TODO: put this into a config file
    params = {
        "objective": "binary",
        "metric": "binary_logloss",
        #"is_unbalance": True,
    }

    threshold = 0.5
    num_boost_round = 250
    train_data = lightgbm.Dataset(x_train, label=y_train)

    classifier = lightgbm.train(params, train_data, num_boost_round=num_boost_round)

    #Testing the accuracy based on the test dataset, which might contain synthetic data 
    y_pred = classifier.predict(x_test, num_iteration=classifier.best_iteration)

    #for (predicted, actual) in zip(y_pred, y_test):
    #    print(f"predicted {predicted} -> actual {actual}")

    y_pred = [1 if pred > threshold else 0 for pred in y_pred]

    accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
    matrix = confusion_matrix(y_true=y_test, y_pred=y_pred)
    print(accuracy)
    print(matrix)

    #Testing the accuracy based on the validation dataset, which represents real world data
    y_pred = classifier.predict(x_val, num_iteration=classifier.best_iteration)
    y_pred = [1 if pred > threshold else 0 for pred in y_pred]

    accuracy = accuracy_score(y_true=y_val, y_pred=y_pred)
    matrix = confusion_matrix(y_true=y_val, y_pred=y_pred)
    print(accuracy)
    print(matrix)

    save(model_path, classifier)



def save(path, model):
    with open(path, "wb") as out_file:
        pickle.dump(model, out_file)

def dataset(path: str) -> tuple[np.ndarray, np.ndarray]:
    with open(path, "r") as file:
        df = pd.read_json(file, lines=True)
        x = df["vec_repr"].to_list()
        y = df["is_damaged"].to_list()
        return (np.array(x), np.array(y))


if __name__ == "__main__":
    main()
