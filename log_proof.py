import os
import time
import hashlib
import requests

# Multichain environment variables
MULTICHAIN_URL = os.getenv('MULTICHAIN_URL')
RPC_USER = 'multichainrpc'
RPC_PASSWORD = 'password'

def connect_to_multichain(max_retries=30, delay=1):
    # First, check if the MultiChain node is ready
    for attempt in range(max_retries):
        try:
            # Check if MultiChain is running
            payload = {
                "method": "getinfo",
                "params": [],
                "id": 1,
                "jsonrpc": "2.0"
            }
            response = requests.post(MULTICHAIN_URL, json=payload, auth=(RPC_USER, RPC_PASSWORD))
            if response.status_code == 200 and response.json().get('result'):
                print("Connected to MultiChain.")
                break
        except requests.exceptions.RequestException:
            print(f"Waiting for MultiChain to be ready... (attempt {attempt + 1}/{max_retries})")
        time.sleep(delay)
    else:
        print("Failed to connect to MultiChain after maximum retries")
        return False

    # check if stream1 exists
    for attempt in range(max_retries):
        try:
            payload = {
                "method": "liststreams",
                "params": ["stream1"],
                "id": 1,
                "jsonrpc": "1.0"
            }
            response = requests.post(MULTICHAIN_URL, json=payload, auth=(RPC_USER, RPC_PASSWORD))
            if response.status_code == 200:
                streams = response.json().get('result', [])
                if any(stream['name'] == 'stream1' for stream in streams):
                    print("Stream 'stream1' is available.")
                    return True
                else:
                    print(f"Stream 'stream1' not found (attempt {attempt + 1}/{max_retries})")
            else:
                print(f"Failed to list streams (attempt {attempt + 1}/{max_retries}): {response.json()}")
        except requests.exceptions.RequestException:
            print(f"Error checking streams (attempt {attempt + 1}/{max_retries})")
        time.sleep(delay)
    
    print("Failed to verify the existence of stream1 after maximum retries")
    return False

# Function to generate SHA256 hash of log data
def _hash_log_entry(log_data):
    """Generate a SHA256 hash of the log data."""
    return hashlib.sha256(log_data.encode()).hexdigest()


# Store log hash on MultiChain (on-chain)
def store_log_hash(log_category, log_data):
    log_hash = _hash_log_entry(log_data)
    print("Attempting to store log hash on blockchain")
    payload = {
        "method": "publish",
        "params": ["stream1", log_category, log_hash],
        "id": 1,
        "jsonrpc": "1.0"
    }

    response = requests.post(MULTICHAIN_URL, json=payload, auth=(RPC_USER, RPC_PASSWORD))
    if response.status_code == 200:
        txid = response.json().get('result')
        print(f"Log hash stored on blockchain. txid: {txid}")
        return txid
    else:
        print(f"Failed to store log hash: {response.json()}")
        return None


# Verify log hash on MultiChain
def verify_log_hash(log_entry):
    chain_txn_id, log_data = log_entry.split('-', 1)
    """Verify the hash of the log data with the stored hash on MultiChain."""
    log_hash = _hash_log_entry(log_data)
    
    payload = {
        "method": "getstreamitem",
        "params": ["stream1", chain_txn_id],
        "id": 1,
        "jsonrpc": "1.0"
    }

    response = requests.post(MULTICHAIN_URL, json=payload, auth=(RPC_USER, RPC_PASSWORD))
    if response.status_code == 200:
        stored_hash = response.json().get('result', {}).get('data', '')
        if log_hash == stored_hash:
            print("Log verified: No tampering detected.")
        else:
            print("Log tampered!")
    else:
        print(f"Failed to verify log: {response.json()}")
