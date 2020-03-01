import os
import sys
import base64

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

from flask import Flask, jsonify, request
from flask_cors import CORS

from afinn import Afinn
import json
import requests

app = Flask(__name__)
CORS(app)

BAD_REQUEST = 400
SUCCESS = 200

project_id = 414357853263
model_id = "ICN5748246790012928"

@app.route("/get-doctors", methods=["POST"])
def read_output():
    print(request)
    data = request.get_json()
    print(data)
    print(type(data))
    print(data.get("latitude"))
    latitude = str(data.get("latitude"))
    longitude = str(data.get("longitude"))
    description = data.get("description")
    with open("api_key.json") as in_json:
        key = json.load(in_json)["key"]

    place_ids_pairs = {}
    textsearch = {}

    A = Afinn()
    output_score = A.score(description)

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

    return json.dumps(output)

@app.route("/")
def hello():
    return "Hello John lad!"

# 'content' is base-64-encoded image data.
@app.route("/submit-image", methods=["POST"])
def get_prediction():
    print("PREDICTION:CALL")
    if "image" not in request.files:
        return "Adhere to format - image: Blob", BAD_REQUEST
    image = request.files["image"].read()
    prediction_client = automl_v1beta1.PredictionServiceClient()
    name = "projects/{}/locations/us-central1/models/{}".format(project_id, model_id)
    payload = {"image": {"image_bytes": image}}
    params = {}
    prediction = prediction_client.predict(name, payload, params)
    response = {}
    disease_mappings = {
        "MEL": "Melanoma",
        "NV": "Melanocytic nevus",
        "BCC": "Basal cell carcinoma",
        "AK": "Actinic keratosis",
        "BKL": "Benign keratosis",
        "DF": "Dermatofibroma",
        "VASC": "Vascular lesion",
        "SCC": "Squamous cell carcinoma",
    }
    for res in prediction.payload:
        disease = disease_mappings[res.display_name]
        response[disease] = int(res.classification.score * 100)

    return response, SUCCESS

if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
        os.getcwd(), "slohacks.json"
    )
    #app.run(debug=True)
    print("MAIN END:")
    app.run(host='0.0.0.0', port=8080, debug=True)
