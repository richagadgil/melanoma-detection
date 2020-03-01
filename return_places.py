from afinn import Afinn
import json
import requests

def read_output(latitude, longitude, description):
    place_ids_pairs = {}
    textsearch = {}

    output_score = sentiment_analysis(description)

    if output_score >= 0:
        query = "dermatologist"

    else:
        query = "urgent care"

    req_get =(
            'https://maps.googleapis.com/maps/api/place/textsearch/json?location=%s,%s&query=%s&key=%s&rankby=distance' % (latitude, longitude, query, key))
 
    x = requests.get(req_get)
    json_data = json.loads(x.text)
    results = json_data["results"]

    if json_data["status"] != "OK":
        return []

    output = []

    for result in results[:5]:
        textsearch[result["name"]] = result    
        place_ids_pairs[result["name"]] = result["place_id"]

    for place in place_ids_pairs:
        req_get =(
            "https://maps.googleapis.com/maps/api/place/details/json?key=%s&place_id=%s" %(key, place_ids_pairs[place]))
        x = requests.get(req_get)
        json_data = json.loads(x.text)
        results = json_data["result"]

        if "name" in results:
            name = results["name"]

        else:
            name = ""

        if "website" in results:
            website = results["website"]

        else:
            website = ""

        if "formatted_address" in results:
            address = results["formatted_address"]

        else:
            address = ""

        if "formatted_phone_number" in results:
            phone_number = results["formatted_phone_number"]
    
        else:
            phone_number = ""
 
        try:
            ref = textsearch[place]["photos"][0]["photo_reference"]
            photo =(
                "https://maps.googleapis.com/maps/api/place/photo?key=%s&photo_reference=%s&maxwidth=400" %(key, ref))

        except:
            photo = ""

        out_dict =  {
                        "name": name, 
                        "website": website,
                        "address": address,
                        "phone_number": phone_number,
                        "photo" : photo
                    }

        output.append(out_dict)

    return output

def sentiment_analysis(sentence):
    A = Afinn()
    output_score = A.score(sentence)
    return output_score

if __name__ == "__main__":
    with open("api_key.json") as in_json:
        key = json.load(in_json)["key"]

    print(key)

    sentence = "oh god am I going to die?"
    sentence1 = "I am so terrified. What am I going to do?"
    sentence2 = "This is scary but I am glad that I caught this early."
    sentence3 = "I am experiencing a lot of pain. My mark is changing colors."
    sentence4 = "I am not sure if it is serious. I just want to be sure."
    sentence5 = "I am so scared. I have been feeling awful and it is just getting worse. Am I going to die?"
    sentence6 = "Oh heartfelt raptures, I have bliss beyond compare. My skin is great."

    latitude = "35.28"
    longitude = "-120.65"

    output = read_output(latitude, longitude, sentence)

    for out in output:
        print(out)
        print()
        print()
