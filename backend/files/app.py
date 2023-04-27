from flask import Flask, request, jsonify
import parser
import methodfi
# from flask_cors import CORS

app = Flask(__name__)
# cors = CORS(app)

@app.route("/process_xml", methods=["POST"])
def process_xml():
    xml = request.json['xml']
    # parse XML and retrieve data to create entities
    corporate_entity_information, payment_data, corporate_accounts = parser.parse(xml['xml'])

    methodfi.main(corporate_entity_information,payment_data,corporate_accounts)

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