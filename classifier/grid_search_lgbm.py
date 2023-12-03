import lightgbm
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score, precision_score
import pickle
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from hdbscan import HDBSCAN, approximate_predict

DATASET_PATH = "../data/dataset_distance_and_location.jsonl"
DATASETS_PKL_PATH = "../data/datasets.pkl"

class Dataset: 
    def __init__(self, x_train, x_test, x_val, y_train, y_test, y_val):
        self.x_train = x_train
        self.x_test = x_test
        self.x_val = x_val
        self.y_train = y_train
        self.y_test = y_test
        self.y_val = y_val

def grid():
    grid = {
        "threshold": [0.4, 0.5, 0.6],
        "num_leaves": [20, 30, 50],
        "num_boost_round": [300, 400, 500],
        "use_smote": [(False, 0), (True, 0.5), (True, 1)],
        "use_under_sampling": [(False, 0), (True, 0.5), (True, 1)],
        "dataset": [0, 1, 2],
    }

    return grid

def train(
    num_boost_round: int, 
    num_leaves: int,
    x_train: np.ndarray,
    y_train: np.ndarray
):
    params = {
        "objective": "binary",
        "num_leaves": num_leaves,
        "metric": "binary_logloss",
        "is_unbalance": True,
    }

    train_data = lightgbm.Dataset(x_train, label=y_train)
    classifier = lightgbm.train(params, train_data, num_boost_round=num_boost_round)
    return classifier

def evaluate(classifier, x_test, y_test, threshold):
    y_pred = classifier.predict(x_test, num_iteration=classifier.best_iteration)
    y_pred = [1 if pred > threshold else 0 for pred in y_pred]

    accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
    matrix = confusion_matrix(y_true=y_test, y_pred=y_pred)
    recall = recall_score(y_true=y_test, y_pred=y_pred)
    precision = precision_score(y_true=y_test, y_pred=y_pred)

    return {
        "accuracy": accuracy,
        "recall": recall,
        "precision": precision,
        "tn": matrix[0][0],
        "fp": matrix[0][1],
        "fn": matrix[1][0],
        "tp": matrix[1][1],
    }

def main():
    data = load(DATASETS_PKL_PATH)
    grd = grid()
    columns = [
        "threshold", 
        "num_boost_round", 
        "use_smote", 
        "use_under_sampling", 
        "dataset", 
        "accuracy", 
        "recall",
        "precision",
        "tn",
        "fp",
        "fn",
        "tp"
    ]

    eval_dt = pd.DataFrame(columns=columns)
    for i, (use_oversampling, os_strategy) in enumerate(grd["use_smote"]):
        for _ in range(10): 
            print(f"Grid search iteration {i} of {len(grd['use_smote'])}")
        for (use_undersampling, us_strategy) in grd["use_under_sampling"]:
            for ds in grd["dataset"]:
                dataset = data[ds]
                x_train = dataset.x_train
                y_train = dataset.y_train

                if use_oversampling:
                    over_sampler = SMOTE(random_state=42, sampling_strategy=os_strategy)
                    x_train, y_train = over_sampler.fit_resample(x_train, y_train)
                
                if use_undersampling and os_strategy != 1:
                    under_sampler = RandomUnderSampler(random_state=42, sampling_strategy=us_strategy)
                    x_train, y_train = under_sampler.fit_resample(x_train, y_train)

                for num in grd["num_boost_round"]:
                    for num_leaves in grd["num_leaves"]:
                        model = train(num, num_leaves, x_train, y_train)
                        for threshold in grd["threshold"]:
                            evaluation = evaluate(model, dataset.x_test, dataset.y_test, threshold)
                            print(evaluation)
                            eval_dt.loc[len(eval_dt)] = [
                                threshold, 
                                num, 
                                use_oversampling, 
                                use_undersampling, 
                                ds, 
                                evaluation["accuracy"], 
                                evaluation["recall"],
                                evaluation["precision"],
                                evaluation["tn"],
                                evaluation["fp"],
                                evaluation["fn"],
                                evaluation["tp"]
                            ]

    eval_dt.to_csv("../data/grid_search_results.csv")

def load(path):
    with open(path, "rb") as in_file:
        return pickle.load(in_file)

def datasets() -> np.ndarray:
    base_x, y = dataset(DATASET_PATH)

    (x_train, x_test, y_train, y_test) = train_test_split(base_x, y, shuffle=True, test_size=0.2)
    (x_train, x_val, y_train, y_val) = train_test_split(x_train, y_train, shuffle=True, test_size=0.2)

    clusterer, probs = probs_by_cluster(x_train, y_train)

    x_train = add_cluster_feature(x_train, clusterer, probs)
    x_test = add_cluster_feature(x_test, clusterer, probs)
    x_val = add_cluster_feature(x_val, clusterer, probs)

    base_dataset = Dataset(x_train, x_test, x_val, y_train, y_test, y_val)

    x_train = remove_lat_lon(x_train)
    x_test = remove_lat_lon(x_test)
    x_val = remove_lat_lon(x_val)

    wo_lat_lon = Dataset(x_train, x_test, x_val, y_train, y_test, y_val)

    x_train = remove_distance(x_train)
    x_test = remove_distance(x_test)
    x_val = remove_distance(x_val)

    wo_distance = Dataset(x_train, x_test, x_val, y_train, y_test, y_val)

    x_train = remove_prob(x_train)
    x_test = remove_prob(x_test)
    x_val = remove_prob(x_val)
    
    wo_prob = Dataset(x_train, x_test, x_val, y_train, y_test, y_val)

    return np.array([base_dataset, wo_lat_lon, wo_distance, wo_prob])

def remove_prob(x):
    res = []
    for i in x:
        i = np.delete(i, 0)
        res.append(i)

    return np.array(res)

def remove_distance(x):
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


def add_cluster_feature(x, clusterer, probs):
    res = []
    for i in x:
        lat = i[4]
        lon = i[3]
        cluster_id = approximate_predict(clusterer, np.array([[lat, lon]]))[0][0]
        prob = probs[probs["cluster_id"] == cluster_id]["prob"].values[0]
        i = np.insert(i, 0, prob)
        res.append(i)

    return np.array(res)

def save(path, model):
    with open(path, "wb") as out_file:
        pickle.dump(model, out_file)

def dataset(path: str) -> tuple[np.ndarray, np.ndarray]:
    with open(path, "r") as file:
        df = pd.read_json(file, lines=True)
        x = df["vec_repr"].to_list()
        y = df["is_damaged"].to_list()
        return (np.array(x), np.array(y))

def probs_by_cluster(x, y):
    df = pd.DataFrame(zip(x, y), columns=["vec_repr", "is_damaged"])

    latitudes = df["vec_repr"].apply(lambda x: x[4])
    longitudes = df["vec_repr"].apply(lambda x: x[3])
    df["latitude"] = latitudes
    df["longitude"] = longitudes 

    ld_assoc: pd.DataFrame = df.loc[:, ["latitude", "longitude", "is_damaged"]]
    lats = ld_assoc["latitude"].to_numpy()
    lons = ld_assoc["longitude"].to_numpy()

    x = np.column_stack((lats, lons))

    clusterer = HDBSCAN(min_cluster_size=20)
    y = clusterer.fit_predict(x)
    clusterer.generate_prediction_data()

    ld_assoc["cluster_id"] = y
    all_clusters = ld_assoc.groupby("cluster_id").size().reset_index(name="overall_size")

    damaged = ld_assoc[ld_assoc["is_damaged"] == 1]
    damaged_clusters = damaged.groupby("cluster_id").size().reset_index(name="damaged_counts")

    merged = all_clusters.merge(damaged_clusters, on="cluster_id", how="left")
    merged["damaged_counts"].fillna(0, inplace=True)
    merged["prob"] = merged["damaged_counts"] / merged["overall_size"]

    return clusterer, merged.loc[:, ["cluster_id", "prob"]]


if __name__ == "__main__":
    main()
