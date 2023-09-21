import hdbscan
import json
import pandas

def main():
    filename = "../data/full_locations_updated.jsonl"
    d_out_file = "../data/d_location_clusters.json"
    nd_out_file = "../data/nd_location_clusters.json"
    d_locations = []
    nd_locations = []

    with open(filename, "r") as file:
        for line in file:
            package = json.loads(line)
            location = package["location"]
            coords = [location["lat"], location["lon"]]

            if package["is_damaged"]:
                d_locations.append(coords)
            else:
                nd_locations.append(coords)

        dl_cluster = cluster(d_locations)
        ndl_cluster = cluster(nd_locations, min_cluster_size=100)

        with open(d_out_file, "w") as out:
            out.write(json.dumps(dl_cluster))
        with open(nd_out_file, "w") as out:
            out.write(json.dumps(ndl_cluster))

def cluster(arr, min_cluster_size=5):
    df = pandas.DataFrame(arr)
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size)
    clusterer.fit(df)
    labels = clusterer.labels_

    out = []
    for _ in range(0, labels.max() + 1):
        out.append([])

    for idx, val in enumerate(arr):
        label = labels[idx]
        if label == -1:
            continue
        out[label].append(val)

    return list(map(avg, out))

def avg(cluster):
    lats = []
    lons = []

    for val in cluster:
        lats.append(val[0])
        lons.append(val[1])

    cluster_len = len(cluster)

    avg_lat = sum(lats) / cluster_len
    avg_lon = sum(lons) / cluster_len

    return [[avg_lat, avg_lon], cluster_len]

if __name__ == "__main__":
    main()
