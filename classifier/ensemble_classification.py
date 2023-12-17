import pickle
import numpy as np
from os import listdir
from lightgbm import Booster 
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn import svm
import config
from functools import reduce

def main():
    dataset_paths = { 
        "x_val": "./validation/x_val",
        "x_val_wol": "./validation/x_val_wol",
        "y_val": "./validation/y_val"
    }

    model_folder = "./models/new/"
    model_names = listdir(model_folder)

    x_val = load(dataset_paths["x_val"])
    x_val_wol = load(dataset_paths["x_val_wol"])
    y_val = load(dataset_paths["y_val"])

    #convert the list of configs to a dict that is indexed by the name of the model 
    models = {}

    cfgs = []
    cfgs.extend(config.lgbm_configs)
    cfgs.extend(config.svm_configs)

    #summing all values up and dividing by the amount of predictors (being the # of models)
    predictions = []

    for model_name in model_names:
        print(f"Loading model: {model_name}")
        model = load(model_folder + model_name)
        cfg = get_config(cfgs, model_name)
        #assuming the model name is unique
        models[model_name] = {
            "model": model,
            "config": cfg, 
        }

        x = x_val if cfg["includes_locations"] else x_val_wol
        y_pred = model.predict(x)

        #binary mapping in case the model is a LightGBM
        #maybe we don't need this
        if isinstance(model, Booster):
            y_pred = [1 if pred > cfg["threshold"] else 0 for pred in y_pred]

        #predictions[model_name]["accuracy"] = accuracy_score(y_val, y_pred)
        #predictions[model_name]["matrix"] = confusion_matrix(y_val, y_pred)
        #predictions[model_name]["y_pred"] = y_pred 
        predictions.append(y_pred)

    #take a weighted average over all predictions and evaluate the accuracy and 
    #confusion matrix

    #because the weighted average could produce arbitrary floating point numbers between 
    #0 and 1 we need a threshold to decide whether the ensemble predicts a zero or a one
    sum_preds = reduce(np.add, predictions)
    threshold = 0.5
    weighted_average = np.divide(sum_preds, len(models))
    weighted_average = [1 if pred > threshold else 0 for pred in weighted_average]

    accuracy = accuracy_score(y_val, weighted_average)
    matrix = confusion_matrix(y_val, weighted_average)

    print(accuracy)
    print(matrix)



def get_config(cfgs: list[dict], name: str) -> dict:
    #returns the first config that matches the given name
    #if the config names are unique there are only one or zero cfgs
    #matching the name
    return next(filter(lambda cfg: cfg["name"] == name, cfgs))

def load(path):
    with open(path, "rb") as file:
        return pickle.load(file)

if __name__ == "__main__":
    main()
