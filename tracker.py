import requests
import json
from datetime import datetime

def get_transactions(address, limit=10):
    url = "https://fullnode.mainnet.sui.io:443"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "suix_queryTransactionBlocks",
        "params": [
            {"fromAddress": address},
            {"limit": limit},
            {"descending_order": True},
            {"options": {"showInput": True, "showEffects": True, "showEvents": True}}
        ]
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Akan raise exception untuk status code error
        data = response.json()
        if 'result' in data and 'data' in data['result']:
            return data['result']['data']
        else:
            print(f"Unexpected response structure. Full response: {json.dumps(data, indent=2)}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error saat melakukan request: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Error saat parsing JSON. Response text: {response.text}")
        return None
    except Exception as e:
        print(f"Error tidak terduga: {e}")
        return None

def parse_transaction(tx):
    tx_type = tx['transaction']['data']['transaction']['kind']
    timestamp = datetime.fromtimestamp(int(tx['timestamp']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
    gas_fee = int(tx['effects']['gasUsed']['computationCost']) / 1_000_000_000
    
    assets = []
    if 'Call' in tx_type:
        for effect in tx['effects']['effects']:
            if 'coinBalanceChange' in effect:
                change = effect['coinBalanceChange']
                amount = int(change['amount']) / 1_000_000_000
                symbol = change['coinType'].split('::')[-1]
                assets.append(f"{'+' if amount > 0 else ''}{amount} {symbol}")
    
    return {
        'type': tx_type,
        'assets': assets,
        'interacted_with': tx['transaction']['data']['sender'],
        'digest': tx['digest'],
        'gas_fee': f"{gas_fee:.9f} SUI",
        'timestamp': timestamp
    }

def main():
    address = input("Enter the Sui address to track: ")
    transactions = get_transactions(address)
    
    if transactions:
        print(f"\nRecent transactions for address {address}:")
        for tx in transactions:
            parsed = parse_transaction(tx)
            print(f"\nType: {parsed['type']}")
            print(f"Assets: {', '.join(parsed['assets'])}")
            print(f"Interacted with: {parsed['interacted_with']}")
            print(f"Digest: {parsed['digest']}")
            print(f"Gas Fee: {parsed['gas_fee']}")
            print(f"Timestamp: {parsed['timestamp']}")
    else:
        print("No transactions found or there was an error fetching the data.")

if __name__ == "__main__":
    main()