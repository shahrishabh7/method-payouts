import requests
import json

def main():
    # connect to Method API
    ensure_connection()

    # create corporate entity
    name = 'Dunkin'
    dba = 'Dunkin'
    ein = 'Dunkin'
    address = '123'
    create_corporate_entity(name,dba,ein,address)

    # connect corporate source accounts
    connect_corporate_accounts(corporation_accounts_information=account)

def ensure_connection():
    url = "https://dev.methodfi.com/ping"

    payload = {}
    headers = {
        'Authorization': 'Bearer sk_UL6hLcNqpATBaAJbygfBHFUP',
        'Cookie': '__cf_bm=6Tt2DbF4GqbUPF6lwmFvekAFSHgJr1k6.JJ7EESbDvI-1682619957-0-AfCze2aZxOOr7wdjpuJCfNtN/MOKg0MVbjUzYwUxos3T7+ihASlCoN+ycEmhFGpPxhBDVlsW+8iGstOoMt0NvKM='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

def create_corporate_entity(name, dba, ein, address):
    url = "https://production.methodfi.com/entities"

    payload = json.dumps({
        "type": "c_corporation",
        "corporation": {
            "name": "{name}",
            "dba": "{dba}",
            "ein": "{ein}",
            "owners": []
        },
        "address": {
            "line1": "{address.line1}",
            "line2": None,
            "city": "{address.city}",
            "state": "{address.state}",
            "zip": "{address.zip}"
        }
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk_UL6hLcNqpATBaAJbygfBHFUP',
        'Cookie': '__cf_bm=VAdkoOoxmeDmjugI7G83vvbPinja3xedb.rtwGasRc8-1682620873-0-Ab9GNQimvR5zKOGvlhEcKJGhuHSJ5qFatIeG/sY+JLzRh2STtpLl2MKl8hjy+uT05xWhnQQim3wqtLeOZ7GmvuQ='
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

# Input should be set of pairs:
# DunkinID : (Routing #, Account #)
def connect_corporate_accounts(corporation_accounts_information):
    for account in corporation_accounts_information.values():
        print(account)


    # url = "https://production.methodfi.com/accounts"

    # payload = json.dumps({
    # "holder_id": "ent_y1a9e1fbnJ1f3",
    # "ach": {
    #     "routing": "367537407",
    #     "number": "57838927",
    #     "type": "checking"
    # }
    # })
    # headers = {
    # 'Content-Type': 'application/json',
    # 'Authorization': 'Bearer sk_UL6hLcNqpATBaAJbygfBHFUP',
    # 'Cookie': '__cf_bm=HQwDN9.vKbxknU3DPKZb44SplYY2ZeVOyKLgqKC8bC4-1682626943-0-AT7mM7MFHZdXtiuNyUsl2NNEMI0/lO2ID/FGfl9uI6KSh34JslZrD4Dme1xGbjqR35LSlEGpFRlsgEj7h3CLGhI='
    # }

    # response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

main()
