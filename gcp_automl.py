import os
import sys
import base64

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BAD_REQUEST = 400
SUCCESS = 200

project_id = 414357853263
model_id = "ICN5748246790012928"

# 'content' is base-64-encoded image data.
@app.route("/submit-image", methods=["POST"])
def get_prediction():
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
    app.run(debug=True)
