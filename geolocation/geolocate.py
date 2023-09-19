import requests
import json
import csv

def main():
    filename = "data/damaged_locations.csv"
    out_file = "data/damaged_locations.jsonl"
    with open(out_file, "a") as out_file:
        with open(filename) as file:
            reader = csv.reader(file, delimiter=",")
            for idx, row in enumerate(reader):
                country = row[0]
                postal = row[1]
                article_type = row[2]
                print(idx, country, postal, article_type)
                stringified = json.dumps(api_request(country, postal, article_type)) + "\n"
                out_file.write(stringified)

#def main(): 
#    ll = get_lat_lon("data/latsandlongs.jsonl")
#    print(ll)

url = "https://nominatim.openstreetmap.org/search?"

def api_request(country, postal, article_type):
    request_url = url + f"country={country}&postalcode={postal}&format=json"
    response = requests.get(request_url)
    responses = response.json()
    lat = -1 
    lon = -1
    if len(responses) > 0: 
        print(responses[0])
        lat = responses[0]["lat"]
        lon = responses[0]["lon"]
        print(lat, lon)

    return {
        "country": country,
        "postal": postal,
        "article": article_type,
        "lat": lat,
        "lon": lon,
    }

def get_lat_lon(filename):
    out = []
    with open(filename, "r") as file:
        for line in file:
            location = json.loads(line)
            if location["response"] == []:
                print("help empty response")
                continue
            lat = location["response"]["lat"]
            lon = location["response"]["lon"]
            out.append([lat, lon])

    return out

if __name__ == "__main__":
    main()
