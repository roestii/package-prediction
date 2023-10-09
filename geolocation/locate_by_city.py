import json
import requests

def main():
    filename = "../data/location_occurence_map.jsonl"
    out_file = "../data/city_damage_ratios.jsonl"
    with open(filename, "r") as file:
        res = list(map(json.loads, file))
        mapped = []
        for idx, place in enumerate(res):
            print(idx)
            city = place["place"] 
            damaged_count = place["counts"]["dc"]
            not_damaged_count = place["counts"]["ndc"]
            lat, lon = api_request(city)
            mapped.append({
                "city": city,
                "lat": lat,
                "lon": lon,
                "dc": damaged_count,
                "ndc": not_damaged_count,
            })

        with open(out_file, "w") as out:
            contents = list(map(lambda x: json.dumps(x) + "\n", mapped))
            out.writelines(contents)
        
def api_request(city):
    url = "https://nominatim.openstreetmap.org/search?"
    request_url = url + f"q={city}&format=json"
    response = requests.get(request_url)
    responses = response.json()
    lat = -1 
    lon = -1
    if len(responses) > 0: 
        lat = responses[0]["lat"]
        lon = responses[0]["lon"]

    return (lat, lon)
 


if __name__ == "__main__":
    main()
