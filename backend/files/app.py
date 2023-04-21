from flask import Flask, request, jsonify
# from flask_cors import CORS

app = Flask(__name__)
# cors = CORS(app)

@app.route("/process_xml", methods=["POST"])
def process_xml():
    xml = request.json['xml']
    print("xml:", xml)
    x = "abc"
    # print / return response -> should be batch of payouts that user can validate
    return x