import json
import pickle
import numpy
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

def main():
    filename = "../data/with_cutted/cutted.jsonl"
    model_path = "./models/leftover_model.pkl"

    (x, y) = dataset_from_path(filename)
    model = model_from_path(model_path)
    
    y_pred = model.predict(x)
    matrix = confusion_matrix(y, y_pred)
    print(matrix)

def model_from_path(path: str) -> RandomForestClassifier:
    with open(path, "rb") as file:
        return pickle.load(file)

def dataset_from_path(path: str) -> tuple[numpy.ndarray, numpy.ndarray]:
    with open(path, "r") as file:
        packages = list(map(json.loads, file))
        xs = list(map(lambda x: x["vec_repr"], packages))
        ys = list(map(lambda x: x["is_damaged"], packages))
        return (numpy.array(xs), numpy.array(ys))


if __name__ == "__main__":
    main()
