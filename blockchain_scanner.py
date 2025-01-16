import argparse
import requests
import time

API_BASE = "https://blockstream.info/api/"

# Fetch transactions using the block hash
def get_block_transactions(block_hash):
    url = f"{API_BASE}block/{block_hash}/txs"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Oops! We encountered an error while fetching transactions for block {block_hash}. Error code: {response.status_code}")
        print("Response details:", response.text)
        return []

    try:
        return response.json()
    except ValueError as e:
        print(f"Something went wrong while parsing the block {block_hash} JSON: {e}")
        print("Response body:", response.text)
        return []

# Fetch the balance for a specific address
def get_balance_for_address(address):
    url = f"{API_BASE}address/{address}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error trying to fetch data for address {address}. We received status code: {response.status_code}")
        print("Details of the response:", response.text)
        return {}

    try:
        return response.json()
    except ValueError as e:
        print(f"Error parsing JSON for address {address}: {e}")
        print("Response body:", response.text)
        return {}

# Fetch the transaction history for a specific address
def get_transactions_for_address(address):
    url = f"{API_BASE}address/{address}/txs"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Oops! Something went wrong while fetching transactions for address {address}. Status code: {response.status_code}")
        print("Response content:", response.text)
        return []

    try:
        return response.json()
    except ValueError as e:
        print(f"Failed to parse transactions for address {address}: {e}")
        print("Response body:", response.text)
        return []

# Get the block hash using the block height
def get_block_hash_by_height(height):
    url = f"{API_BASE}block-height/{height}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve block hash for height {height}. Error code: {response.status_code}")
        print("Error details:", response.text)
        return None

    return response.text.strip()

# Log address to file if it meets certain conditions
def log_address_to_file(address):
    with open("result.txt", "a") as result_file:
        result_file.write(f"Address: {address}\n\n")

# Main function to check addresses within a range of blocks
def check_addresses_in_blocks(start_block, end_block, min_balance_btc=1, min_transaction_year=2013):
    min_balance_satoshi = min_balance_btc * 100_000_000  # Convert BTC to satoshis

    for block_height in range(start_block, end_block + 1):
        print(f"Analyzing block {block_height}...")

        block_hash = get_block_hash_by_height(block_height)
        if not block_hash:
            continue

        transactions = get_block_transactions(block_hash)
        recorded_addresses = set()

        for tx in transactions:
            for vin in tx.get("vin", []):
                prevout = vin.get("prevout")
                if prevout and isinstance(prevout, dict):
                    address = prevout.get("scriptpubkey_address", "")
                    if address:
                        print(f"Found a potential address: {address}")

                        if address in recorded_addresses:
                            continue  # Skip if we've already seen this address

                        balance_info = get_balance_for_address(address)
                        if balance_info:
                            funded_txo_sum = balance_info.get('chain_stats', {}).get('funded_txo_sum', 0)
                            spent_txo_sum = balance_info.get('chain_stats', {}).get('spent_txo_sum', 0)
                            balance_in_satoshis = funded_txo_sum - spent_txo_sum
                            print(f"Balance for address {address}: {balance_in_satoshis} satoshis")

                            if balance_in_satoshis < min_balance_satoshi:
                                print(f"Address {address} has less than {min_balance_btc} BTC. Skipping.")
                                continue

                        tx_history = get_transactions_for_address(address)
                        if tx_history:
                            last_tx = tx_history[0]
                            timestamp = last_tx.get('status', {}).get('block_time', None)

                            if timestamp:
                                if isinstance(timestamp, int):
                                    formatted_time = time.gmtime(timestamp)
                                    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", formatted_time)

                                tx_time = time.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
                                tx_year = time.strftime("%Y", tx_time)

                                if int(tx_year) < min_transaction_year:
                                    print(f"Last transaction for {address} occurred before {min_transaction_year}. Logging address.")
                                    log_address_to_file(address)
                                    recorded_addresses.add(address)
                                else:
                                    print(f"Last transaction for {address} occurred after {min_transaction_year}. Skipping.")
                            else:
                                print(f"No timestamp available for address {address}.")
                        else:
                            print(f"No transactions found for address {address}. Continuing...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Bitcoin addresses in blocks.")
    parser.add_argument("-s", "--start-block", type=int, required=True, help="Starting block height.")
    parser.add_argument("-e", "--end-block", type=int, required=True, help="Ending block height.")
    parser.add_argument("-b", "--min-balance", type=float, required=True, help="Minimum balance in BTC.")
    parser.add_argument("-y", "--min-year", type=int, required=True, help="Minimum year for the last transaction.")

    args = parser.parse_args()

    check_addresses_in_blocks(
        start_block=args.start_block,
        end_block=args.end_block,
        min_balance_btc=args.min_balance,
        min_transaction_year=args.min_year
    )
