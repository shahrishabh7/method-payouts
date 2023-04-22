from flask import Flask, request, jsonify
import parser
# from flask_cors import CORS

app = Flask(__name__)
# cors = CORS(app)

@app.route("/process_xml", methods=["POST"])
def process_xml():
    xml = request.json['xml']
    # print(xml)
    print(type(xml['xml']))
    parser.parse(xml['xml'])
    # print / return response -> should be batch of payouts that user can validate
    response = jsonify({"response": "success!"})
    return response

@app.route('/profile', methods=["GET"])
def my_profile():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body