import requests
import json
import csv

def main():
    filename = "data/latsandlongs.csv"
    out_file = "data/latsandlongs.jsonl"
    with open(out_file, "a") as out_file:
        with open(filename) as file:
            reader = csv.reader(file, delimiter=",")
            for idx, row in enumerate(reader):
                print(idx)
                country = row[0]
                postal = row[1]
                stringified = json.dumps(api_request(country, postal)) + "\n"
                out_file.write(stringified)

#def main(): 
#    get_lat_lon("data/latsandlongs.jsonl")

url = "https://nominatim.openstreetmap.org/search?"

def api_request(country, postal):
    request_url = url + f"country={country}&postalcode={postal}&format=json"
    response = requests.get(request_url)
    responses = response.json()
    if len(responses) == 0: 
        responses = []
    else:
        responses = responses[0]

    return {
        "country": country,
        "postal": postal,
        "response": responses
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

if __name__ == "__main__":
    main()
