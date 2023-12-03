import lightgbm
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from hdbscan import HDBSCAN, approximate_predict

def main():
    model_path = "./models/lgbm_t05_n250_wdapal.pkl"
    #dataset_path = "../data/with_cutted/leftover.jsonl"
    dataset_path = "../data/dataset_distance_and_location.jsonl"
    #validation_path = "../data/with_cutted/cutted.jsonl"

    (x, y) = dataset(dataset_path)
    #(x_val, y_val) = dataset(validation_path)
    (x_train, x_test, y_train, y_test) = train_test_split(x, y, shuffle=True, test_size=0.2)
    (x_train, x_val, y_train, y_val) = train_test_split(x_train, y_train, shuffle=True, test_size=0.2)

    clusterer, probs = probs_by_cluster(x_train, y_train)

    x_train = add_cluster_feature(x_train, clusterer, probs)
    x_test = add_cluster_feature(x_test, clusterer, probs)
    x_val = add_cluster_feature(x_val, clusterer, probs)

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
        "is_unbalance": True,
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


def add_cluster_feature(x, clusterer, probs):
    res = []
    for i in x:
        lat = i[4]
        lon = i[3]
        i = np.delete(i, 3)
        i = np.delete(i, 3)
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
