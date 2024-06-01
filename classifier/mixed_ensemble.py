import pickle
from lgbm import lightgbm
import pandas as pd
import numpy as np
import lightgbm
from sklearn import svm
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import config

def main():
    model_path = "./models/new/"
    dataset_path = "../data/dataset_with_locations.jsonl"
    x, y = load_dataset(dataset_path)
    x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle=True, test_size=0.2)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, shuffle=True, test_size=0.2)

    x_train_wol = np.array(list(map(cut_locations, x_train)))
    x_test_wol = np.array(list(map(cut_locations, x_test)))
    x_val_wol = np.array(list(map(cut_locations, x_val)))

    save(x_val_wol, "./validation/x_val_wol")
    save(x_val, "./validation/x_val")
    save(y_val, "./validation/y_val")

    lgbm_models = {}
    svm_models = {}

    for cfg in config.lgbm_configs:
        name = cfg["name"]
        print(f"Training {name}")
        #Set the training data according to the config (including locations or excluding locations)
        x = x_train if cfg["includes_locations"] else x_train_wol
        x_t = x_test if cfg["includes_locations"] else x_test_wol

        model = lgbm_model(cfg, x, y_train)
        accuracy, matrix = evaluate(model, x_t, y_test, threshold=cfg["threshold"])
        print(f"Model {name}; Accuracy: {accuracy}")
        print(f"Model {name}; Confusion matrix: {matrix}")
        #Assuming that the names of the models are unique
        lgbm_models[cfg["name"]] = model
        save(model, model_path + name)

    for cfg in config.svm_configs:
        name = cfg["name"]
        print(f"Training {name}")
        #Set the training data according to the config (including locations or excluding locations)
        x = x_train if cfg["includes_locations"] else x_train_wol
        x_t = x_test if cfg["includes_locations"] else x_test_wol

        model = svm_model(cfg, x, y_train)
        accuracy, matrix = evaluate(model, x_t, y_test)
        print(f"Model {name}; Accuracy: {accuracy}")
        print(f"Model {name}; Confusion matrix: {matrix}")
        #Assuming that the names of the models are unique
        svm_models[cfg["name"]] = model
        save(model, model_path + name)

    #classifier = lgbm_model(config, x_train, y_train)
    #y_pred = classifier.predict(x_test, num_iteration=classifier.best_iteration)
    #y_pred = [1 if pred > config["threshold"] else 0 for pred in y_pred]
    #accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
    #matrix = confusion_matrix(y_true=y_test, y_pred=y_pred)
    #print(accuracy)
    #print(matrix)

    #models = [
    #    "./models/lgbm_t04_n250_wol.pkl"
    #    "./models/lgbm_t03_n500_wl.pkl"
    #]

    #models = list(map(load_model, models))
def evaluate(model: svm.SVC | lightgbm.Booster, x_test, y_test, threshold=None) -> tuple[float, np.ndarray]:
    y_pred = model.predict(x_test)

    #when there is a threshold update the predictions such that the output only contains binary values
    if threshold is not None:
        y_pred = [1 if pred > threshold else 0 for pred in y_pred]

    accuracy = accuracy_score(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)

    return (accuracy, matrix)

def svm_model(cfg, x_train, y_train):
    classifier = svm.SVC(class_weight=cfg["class_weight"], kernel=cfg["kernel"])
    classifier.fit(x_train, y_train)
    return classifier

def cut_locations(x: np.ndarray) -> np.ndarray:
    """
    Removes the elements that correspond to the location (latitude and longitude) {2, 3}
    """

    location_idx = [2, 3]
    return np.delete(x, location_idx)

def save(model, path):
    with open(path, "wb") as out_file:
        pickle.dump(model, out_file)


def load_dataset(path: str) -> tuple[np.ndarray, np.ndarray]:
    with open(path, "r") as file:
        df = pd.read_json(file, lines=True)
        x = df["vec_repr"].to_list()
        y = df["is_damaged"].to_list()
        return (np.array(x), np.array(y))

def load_model(model_path):
    with open(model_path, "rb") as file:
        return pickle.load(file)

def lgbm_model(cfg, x_train, y_train):
    if "over_sampler" in cfg.keys():
        x_train, y_train = cfg["over_sampler"].fit_resample(x_train, y_train)
    if "under_sampler" in cfg.keys():
        x_train, y_train = cfg["under_sampler"].fit_resample(x_train, y_train)

    train_data = lightgbm.Dataset(x_train, label=y_train)
    classifier = lightgbm.train(cfg["params"], train_data, num_boost_round=cfg["num_boost_round"])
    return classifier
    

if __name__ == "__main__":
    main()
