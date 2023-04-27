import requests



def ensure_connection():
    url = "https://dev.methodfi.com/ping"

    payload = {}
    headers = {
    'Authorization': 'Bearer sk_UL6hLcNqpATBaAJbygfBHFUP',
    'Cookie': '__cf_bm=6Tt2DbF4GqbUPF6lwmFvekAFSHgJr1k6.JJ7EESbDvI-1682619957-0-AfCze2aZxOOr7wdjpuJCfNtN/MOKg0MVbjUzYwUxos3T7+ihASlCoN+ycEmhFGpPxhBDVlsW+8iGstOoMt0NvKM='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def main():
    # connect to Method API
    ensure_connection()

    

main()