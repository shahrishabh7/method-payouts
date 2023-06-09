import requests
import json
from datetime import datetime
from threading import Thread
import pandas as pd
from collections import defaultdict

def create_entities_and_accounts(individual_entity_information, corporate_entity_information, payment_data, corporation_accounts_information):

    # ensure connection to Method API
    ensure_connection()

    # create corporate entity
    entity_id = create_corporate_entity(corporate_entity_information)

    # connect 5 corporate source accounts
    connect_corporate_accounts(corporation_accounts_information,entity_id)

    # create individual entities
    individual_entity_dict = create_individual_entities(individual_entity_information)

    # connect individual accounts
    # get dataframe of holderID, merchantID, and account #
    individual_acccounts_df = get_individual_account_dataframe(payment_data,individual_entity_dict)
    connect_individual_accounts(individual_acccounts_df)

def make_payments(payment_data):
    url = "https://dev.methodfi.com/payments"

    for payment in payment_data:
        payload = json.dumps({
        "amount": 5000,
        "source": f"{payment['source']}",
        "destination": f"{payment['destination']}",
        "description": "Loan Pmt"
        })
        headers = {
        'Authorization': 'Bearer sk_UL6hLcNqpATBaAJbygfBHFUP',
        'Content-Type': 'application/json',
        'Cookie': '__cf_bm=DNoZXPwpdoL0rCn_ofOdYFdlGU1Gq.zM4sEkW5pnZEc-1683141038-0-AUJC1sAOCUgmkkXEogyu6uZ/jM9c8zRbbgPmlPW2MkrKiRshWnlDOUlT7VCH4TnjE42pXBD3jViTfJreYneDpYg='
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

    return
        
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
    url = "https://dev.methodfi.com/entities"

    name = corporate_entity_information['Name']
    dba = corporate_entity_information['DBA']
    ein = corporate_entity_information['EIN']
    addressline1 = corporate_entity_information['Address Line 1']
    city = corporate_entity_information['City']
    state = corporate_entity_information['State']
    zip = corporate_entity_information['Zip']

    payload = json.dumps({
        "type": "llc",
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
            "zip": f"{52403}"
        }
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk_UL6hLcNqpATBaAJbygfBHFUP',
        'Cookie': '__cf_bm=VAdkoOoxmeDmjugI7G83vvbPinja3xedb.rtwGasRc8-1682620873-0-Ab9GNQimvR5zKOGvlhEcKJGhuHSJ5qFatIeG/sY+JLzRh2STtpLl2MKl8hjy+uT05xWhnQQim3wqtLeOZ7GmvuQ='
    }

    # convert response to json and parse for entity ID, return entity ID
    response = requests.request("POST", url, headers=headers, data=payload)
    response = response.json()
    return response['data']['id']

# Input should be set of pairs:
# DunkinID : (Routing #, Account #)
def connect_corporate_accounts(corporation_accounts_information,entity_id):
    url = "https://dev.methodfi.com/accounts"
    for accountID, accountNumbers in corporation_accounts_information.items():
        payload = json.dumps({
            "holder_id": f"{entity_id}",
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

# create individual entities using multithreading to run 30 threads at once
def create_individual_entities(individual_entity_information):
    individual_entity_dict = dict()
    url = "https://dev.methodfi.com/entities"
    column_names = list(individual_entity_information.keys())
    threads = []  # create a list to store the threads
    num_threads = 300  # set the number of threads to use

    def make_api_call(i):
        dob = convert_date_format(individual_entity_information['E: DOB'][i])
        payload = json.dumps({
            "type": "individual",
            "individual": {
                "first_name": f"{individual_entity_information['E: First Name'][i]}",
                "last_name": f"{individual_entity_information['E: Last Name'][i]}",
                "phone": f"{individual_entity_information['E: Phone Number'][i]}",
                "dob": f"{dob}"
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer sk_UL6hLcNqpATBaAJbygfBHFUP',
            'Cookie': '__cf_bm=UOHWXnJcTzM2pgRwySFP4d3T9px_2HhHDLfbyRBS8eU-1682633226-0-Ad+znSLg72DuvBzYBH7N0O74DRLQXRt1tlps/HrqWClLUcV5G/rtngWtBVOIs+g0D/2nMZOMFreGDGEg2CYLJy4='
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        print(response)

        full_name = individual_entity_information['E: First Name'][i] + ' ' + individual_entity_information['E: Last Name'][i]
        individual_entity_dict[full_name] = response["data"]["id"]

    for i in range(len(individual_entity_information[column_names[0]])):
        print(i)
        t = Thread(target=make_api_call, args=(i,))
        threads.append(t)
        if len(threads) == num_threads:  # start the threads when the max number is reached
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            threads = []

    # start and join any remaining threads
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return individual_entity_dict

def connect_individual_accounts(payment_data):
    pass

def get_individual_account_dataframe(payment_data,individual_entity_dict):
    merchants = get_merchants()
    merchant_id_dict = defaultdict(int)
    for merchant in merchants:
        plaid_ids = merchant["provider_ids"]["plaid"]
        for id in plaid_ids:
            merchant_id_dict[id] = merchant["mch_id"]

    print(merchant_id_dict)
    # Info needed in df
    # id of entity that owns account
    # merchant_id
    # loan_account_number

    payment_df = pd.DataFrame(payment_data)
    filtered_df = payment_df[['E: First Name', 'E: Last Name', 'E: Payee Plaid Id', 'E: Payee Loan Account #']].copy()
    filtered_df['Full Name'] = filtered_df['E: First Name'] + ' ' + filtered_df['E: Last Name']

    index_length = len(filtered_df.index)
    merchant_ids = [''] * index_length
    filtered_df['Merchant ID'] = merchant_ids

    for index, row in filtered_df.iterrows():
        # print(row['E: Payee Plaid Id'])
        filtered_df['Merchant ID'] = merchant_id_dict[row['E: Payee Plaid Id']]

    filtered_df.to_csv('payment_df.csv', index=False)
    return

def get_merchants():
    url = "https://dev.methodfi.com/merchants"

    payload = {}
    headers = {
    'Authorization': 'Bearer: sk_UL6hLcNqpATBaAJbygfBHFUP',
    'Cookie': '__cf_bm=Wb8uq3uyo1k6pv8vRkLRiVc47hTI3Htp5VJzAKL_JFc-1683059108-0-ASKRr0G6mpSzWiaRs3ThgD6ON2CG7Lpm2KikEkQX7SVxYd5NFbP4fDLmj7o0veDcwGXD15Jjjuq2uw0Yh4iJv70='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    return response.json()["data"]

def convert_date_format(date_string):
    # Convert the string to a datetime object
    date_obj = datetime.strptime(date_string, '%m-%d-%Y')

    # Convert the datetime object back to a string in the desired format
    new_date_string = date_obj.strftime('%Y-%m-%d')

    return new_date_string