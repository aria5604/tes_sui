import requests
import json
from collections import defaultdict

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

def simplify_token_name(token_type):
    # Extract the last part of the token type as a simplified name
    return token_type.split("::")[-1]

def format_balance(balance):
    # Convert balance to a decimal number with 9 decimal places
    return f"{balance / 1_000_000_000:.9f}"

def main():
    address = input("Enter the Sui address to check: ")
    tokens = get_tokens(address)
    
    if tokens:
        token_balances = defaultdict(int)
        
        for token in tokens:
            token_type = token['data']['type']
            balance = int(token['data']['content']['fields']['balance'])
            simplified_name = simplify_token_name(token_type)
            token_balances[simplified_name] += balance
        
        print(f"\nToken balances for address {address}:")
        for token, balance in token_balances.items():
            formatted_balance = format_balance(balance)
            print(f"{formatted_balance} {token}")
        
        # Special case for FOMO token
        if "FOMO" not in token_balances:
            print("0.000000000 FOMO")
    else:
        print("No tokens found or there was an error fetching the data.")

if __name__ == "__main__":
    main()