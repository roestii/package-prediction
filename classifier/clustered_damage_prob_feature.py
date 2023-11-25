import pandas as pd
import numpy as np
from hdbscan import HDBSCAN
from pandas.core.reshape.api import merge

def main():
    path = "../data/dataset_distance_and_location.jsonl"
    df = pd.read_json(path, lines=True)

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

    ld_assoc["cluster_id"] = y
    all_clusters = ld_assoc.groupby("cluster_id").size().reset_index(name="overall_size")

    damaged = ld_assoc[ld_assoc["is_damaged"] == 1]
    damaged_clusters = damaged.groupby("cluster_id").size().reset_index(name="damaged_counts")

    merged = all_clusters.merge(damaged_clusters, on="cluster_id", how="left")
    merged["damaged_counts"].fillna(0, inplace=True)
    merged["prob"] = merged["damaged_counts"] / merged["overall_size"]

    # TODO: only calculate the probability based on the training data set entries

if __name__ == "__main__":
    main()

