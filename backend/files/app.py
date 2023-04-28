from flask import Flask, request, jsonify
import parser
import methodfi
# from flask_cors import CORS

app = Flask(__name__)
# cors = CORS(app)

# Endpoint to process XML, create Method entities and accounts, and return staged payments to front-end for preview
@app.route("/process_xml", methods=["POST"])
def process_xml():
    xml = request.json['xml']
    # parse XML and retrieve data to create entities
    payments_preview, individual_entity_information, corporate_entity_information, payment_data, corporate_accounts = parser.parse(
        xml['xml'])

    # create entities and accounts
    # methodfi.create_entities_and_accounts(
    #     individual_entity_information, corporate_entity_information, payment_data, corporate_accounts)

    # print / return response -> should be batch of payouts that user can validate
    response = jsonify({
        'payments_preview':payments_preview,
        'payment_data':payment_data
    })
    return response

# hit this endpoint after payment batch is confirmed
@app.route("/process_payments", methods=["POST"])
def process_payments():
    pass

@app.route('/profile', methods=["GET"])
def my_profile():
    response_body = {
        "name": "Nagato",
        "about": "Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body
