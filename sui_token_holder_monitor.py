import requests
import json
import time
from collections import defaultdict
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_token_holders(token_type):
    url = "https://fullnode.mainnet.sui.io:443"
    
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "suix_getDynamicFields",
        "params": [
            token_type,
            None,
            None
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

def get_balance(address):
    url = "https://fullnode.mainnet.sui.io:443"
    
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "suix_getBalance",
        "params": [
            address,
            "0x2::sui::SUI"
        ]
    })
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 200:
        data = response.json()
        return int(data['result']['totalBalance'])
    else:
        return 0

def main():
    token_type = input("Enter the token type to monitor (e.g., 0x2::sui::SUI): ")
    
    while True:
        holders = get_token_holders(token_type)
        
        if holders:
            balances = defaultdict(int)
            total_balance = 0
            
            for holder in holders:
                address = holder['objectId']
                balance = get_balance(address)
                balances[address] += balance
                total_balance += balance
            
            clear_screen()
            print(f"Token Holders for {token_type}")
            print("=" * 50)
            print(f"{'Address':<42} | {'Balance':<15} | {'Percentage':<10}")
            print("-" * 50)
            
            for address, balance in sorted(balances.items(), key=lambda x: x[1], reverse=True):
                percentage = (balance / total_balance) * 100 if total_balance > 0 else 0
                print(f"{address:<42} | {balance:<15} | {percentage:.2f}%")
            
            print("=" * 50)
            print(f"Total Balance: {total_balance}")
        else:
            print("Error fetching token holders data.")
        
        time.sleep(2)

if __name__ == "__main__":
    main()
