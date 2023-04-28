import requests
import json

def create_entities_and_accounts(individual_entity_information, corporate_entity_information, payment_data, corporation_accounts_information):

    # connect to Method API
    ensure_connection()

    # create corporate entity
    create_corporate_entity(corporate_entity_information)

    # connect 5 corporate source accounts
    connect_corporate_accounts(corporation_accounts_information)

    # create individual entities
    # create_individual_entities(individual_entity_information)

    # connect individual accounts
    # connect_individual_accounts(payment_data)

def make_payments():
    pass

def ensure_connection():
    url = "https://dev.methodfi.com/ping"

    payload = {}
    headers = {
        'Authorization': 'Bearer sk_UL6hLcNqpATBaAJbygfBHFUP',
        'Cookie': '__cf_bm=6Tt2DbF4GqbUPF6lwmFvekAFSHgJr1k6.JJ7EESbDvI-1682619957-0-AfCze2aZxOOr7wdjpuJCfNtN/MOKg0MVbjUzYwUxos3T7+ihASlCoN+ycEmhFGpPxhBDVlsW+8iGstOoMt0NvKM='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    return

def create_corporate_entity(corporate_entity_information):
    print(corporate_entity_information)
    url = "https://production.methodfi.com/entities"

    name = corporate_entity_information['Name']
    dba = corporate_entity_information['DBA']
    ein = corporate_entity_information['EIN']
    addressline1 = corporate_entity_information['Address Line 1']
    city = corporate_entity_information['City']
    state = corporate_entity_information['State']
    zip = corporate_entity_information['Zip']

    payload = json.dumps({
        "type": "c_corporation",
        "corporation": {
                "name": f"{name}",
                "dba": f"{dba}",
                "ein": f"{ein}",
                "owners": []
        },
        "address": {
            "line1": f"{addressline1}",
            "line2": None,
            "city": f"{city}",
            "state": f"{state}",
            "zip": f"{zip}"
        }
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk_UL6hLcNqpATBaAJbygfBHFUP',
        'Cookie': '__cf_bm=VAdkoOoxmeDmjugI7G83vvbPinja3xedb.rtwGasRc8-1682620873-0-Ab9GNQimvR5zKOGvlhEcKJGhuHSJ5qFatIeG/sY+JLzRh2STtpLl2MKl8hjy+uT05xWhnQQim3wqtLeOZ7GmvuQ='
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    return

# Input should be set of pairs:
# DunkinID : (Routing #, Account #)ß
def connect_corporate_accounts(corporation_accounts_information):
    url = "https://production.methodfi.com/accounts"
    for accountID, accountNumbers in corporation_accounts_information.items():
        payload = json.dumps({
            "holder_id": f"{accountID}",
            "ach": {
                "routing": f"{accountNumbers[0]}",
                "number": f"{accountNumbers[1]}",
                "type": "checking"
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer sk_UL6hLcNqpATBaAJbygfBHFUP',
            'Cookie': '__cf_bm=HQwDN9.vKbxknU3DPKZb44SplYY2ZeVOyKLgqKC8bC4-1682626943-0-AT7mM7MFHZdXtiuNyUsl2NNEMI0/lO2ID/FGfl9uI6KSh34JslZrD4Dme1xGbjqR35LSlEGpFRlsgEj7h3CLGhI='
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

    return

def create_individual_entities(individual_entity_information):
    url = "https://production.methodfi.com/entities"
    column_names = list(individual_entity_information.keys())

    for i in range(len(individual_entity_information[column_names[0]])):
        payload = json.dumps({
        "type": "individual",
        "individual": {
            "first_name": f"{individual_entity_information['E: First Name'][i]}",
            "last_name": f"{individual_entity_information['E: Last Name'][i]}",
            "phone": f"{individual_entity_information['E: Phone Number'][i]}",
            "dob": f"{individual_entity_information['E: DOB'][i]}"
        }
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk_UL6hLcNqpATBaAJbygfBHFUP',
        'Cookie': '__cf_bm=UOHWXnJcTzM2pgRwySFP4d3T9px_2HhHDLfbyRBS8eU-1682633226-0-Ad+znSLg72DuvBzYBH7N0O74DRLQXRt1tlps/HrqWClLUcV5G/rtngWtBVOIs+g0D/2nMZOMFreGDGEg2CYLJy4='
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

    return