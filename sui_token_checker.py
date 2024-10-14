import requests
import json

def get_tokens(address):
    url = "https://fullnode.mainnet.sui.io:443"
    
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "suix_getOwnedObjects",
        "params": [
            address,
            {
                "filter": {
                    "StructType": "0x2::coin::Coin"
                },
                "options": {
                    "showType": True,
                    "showContent": True
                }
            }
        ]
    })
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 200:
        data = response.json()
        return data['result']['data']
    else:
        return None

def main():
    address = input("Enter the Sui address to check: ")
    tokens = get_tokens(address)
    
    if tokens:
        print(f"Tokens found for address {address}:")
        for token in tokens:
            token_type = token['data']['type']
            balance = token['data']['content']['fields']['balance']
            print(f"Type: {token_type}, Balance: {balance}")
    else:
        print("No tokens found or there was an error fetching the data.")

if __name__ == "__main__":
    main()
