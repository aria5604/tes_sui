import requests
import json

def test_sui_api(address):
    url = "https://fullnode.mainnet.sui.io:443"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "suix_queryTransactionBlocks",
        "params": [
            {"fromAddress": address},
            {"limit": 10},
            True,
            {"showInput": True, "showEffects": True, "showEvents": True}
        ]
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Response Body: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    address = input("Enter the Sui address to test: ")
    test_sui_api(address)