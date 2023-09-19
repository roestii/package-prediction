import hdbscan
import pandas
import json

def avg(cluster):
    lats = list(map(lambda x: x[0], cluster))
    lons = list(map(lambda x: x[1], cluster))

    lat_avg = sum(lats) / len(lats)
    lon_avg = sum(lons) / len(lons)

    return [[lat_avg, lon_avg], len(cluster)]

def cluster(vals):
    if len(vals) <= 15:
        return list(map(lambda val: [val, 1], vals)) 
    df = pandas.DataFrame(vals)
    clusterer = hdbscan.HDBSCAN()
    clusterer.fit(vals)
    labels = clusterer.labels_
    
    clusters = []
    for i in range(0, labels.max() + 1):
        clusters.append([])

    for i in range(0, len(vals)):
        label = labels[i]
        if label == -1:
            continue

        clusters[label].append(vals[i])

    return list(map(avg, clusters))

def create_map(lines):
    init = {}
    for line in lines: 
        data = json.loads(line)
        article = data["article"]
        coords = [float(data["lat"]), float(data["lon"])]

        if coords == [-1, -1]:
            continue

        if article in init.keys():
            init[article].append(coords)
        else:
            init[article] = [coords]
    return init

def main(): 
    filename = "../data/damaged_locations.jsonl"
    with open(filename, "r") as file:
        article_map = create_map(file)
        avg_map = {}
        for key in article_map.keys():
            clusters = cluster(article_map[key])
            avg_map[key] = clusters
        with open("../data/clustered.json", "w") as out_file:
            out_file.write(json.dumps(avg_map))

if __name__ == "__main__":
    main()
