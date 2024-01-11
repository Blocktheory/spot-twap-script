from dotenv import load_dotenv

load_dotenv()

CHAIN_ID_OP = "op"
CHAIN_ID_ETH = "eth"
CHAIN_ID_BNB = "bnb"
CHAIN_ID_SOL = "sol"


def calculate_order_quantity(quantity, duration_hours, interval):
    try:
        quantity = float(quantity)
        duration_hours = float(duration_hours)
        interval = float(interval)
    except:
        return 0
    if interval <= 0:
        return 0
    interval_seconds = interval * 60  # converting to seconds
    total_intervals = duration_hours * 3600 / interval_seconds
    return round(quantity / total_intervals, 2)


def sanity_check(dex, token_pair_symbol, trade_type, order_quantity, duration_hours, interval_minutes, address, chain, key):
    if not dex or dex.lower() not in ["gate", "binance", "mexc", "uniswap", "jupiter"]:
        print("Enter valid dex (gate, binance, mexc, uniswap)")
        return False
    if not token_pair_symbol:
        print("Enter valid token pair")
        return False
    if not order_quantity or order_quantity <= 0:
        print("Enter quantity is less than 0.01 for each interval, make sure to increase the quantity")
        return False
    if not interval_minutes or interval_minutes < 0.1:
        print("Enter valid interval minutes, make sure its greater than 0.1")
        return False
    if not duration_hours or duration_hours < 0.1:
        print("Enter valid duration in hours, make sure its greater than 0.1")
        return False
    if not trade_type or trade_type.lower() not in ["buy", "sell"]:
        print("Enter valid trade type buy or sell")
        return False
    if chain and chain.lower() not in [CHAIN_ID_ETH, CHAIN_ID_OP, CHAIN_ID_BNB, CHAIN_ID_SOL]:
        print("Enter valid chain id (eth, op, bnb, sol)")
        return False
    if address and (dex == "uniswap" or dex == "jupiter"):
        if dex == "jupiter":
            is_valid = is_valid_eth_address(address)
        else:
            is_valid = is_valid_eth_address(address)
        if not is_valid:
            print("Enter valid address to trade")
            return False
    if key and (dex == "uniswap" or dex == "jupiter"):
        if dex == "jupiter":
            is_valid = is_valid_eth_private_key(key)
        else:
            is_valid = is_valid_eth_private_key(key)
        if not is_valid:
            print("Enter valid private key to trade")
            return False
    return True


def get_user_input():
    dex = input(
        "Choose your exchange platform binance or gate or mexc or uniswap or jupiter: ")
    symbol = input("Enter the trading pair symbol (e.g., 'BNBUSDT'): ")
    trade_type = input("Specify the trade type to buy or sell: ")
    quantity = input("Enter the quantity to trade (units): ")
    duration = input("Specify the duration of the order in hours: ")
    interval = input("Enter the interval for each TWAP in minutes: ")
    address = None
    chain = None
    key = None
    if dex == "uniswap" or dex == "jupiter":
        chain = input(
            "Enter the chain Id you want to trade on eth, bnb, op, sol (optional): ")
        address = input("Enter the address you want to send (optional): ")
        if address != None and address != "":
            key = input(
                "Enter the private key of the address (we're not saving any info - optional): ")
    return dex, symbol, trade_type, quantity, duration, interval, address, chain, key

def load_tokens(file_path):
    import json
    with open(file_path, "r") as file:
        return json.load(file)


def fetch_token_data(chain=CHAIN_ID_ETH):
    print("chain ", chain)
    path = "./constants/tokens/eth.json"
    if chain == CHAIN_ID_OP:
        path = "./constants/tokens/op.json"
    elif chain == CHAIN_ID_BNB:
        path = "./constants/tokens/bnb.json"
    elif chain == CHAIN_ID_SOL:
        path = "./constants/tokens/sol.json"
    return load_tokens(path)

def split_known_token_pair(pair, tokens_data=[]):
    for token in tokens_data:
        symbol = token['symbol'].lower()
        if pair.lower().startswith(symbol):
            symbol2 = pair[len(symbol):]
            return symbol, symbol2
    return pair, None

def get_token_details(token_combination, chain=CHAIN_ID_ETH):
    tokens_data = fetch_token_data(chain)
    if "_" in token_combination:
        # Split the input to get individual tokens
        token1, token2 = token_combination.split("_")
    else:
        # Try to fetch tokens from the list
        token1, token2 = split_known_token_pair(
            token_combination, tokens_data)
    # Define a helper function to find a token in the tokens data
    def find_token(token, tokens_data):
        if not token is None:
            for token_data in tokens_data:
                if token.lower() in [token_data["symbol"].lower(), token_data["address"].lower()]:
                    return token_data
        return None

    # Find each token
    token1_details = find_token(token1, tokens_data)
    token2_details = find_token(token2, tokens_data)
    return token1_details, token2_details

def is_valid_eth_address(address):
    import re
    if not isinstance(address, str):
        return False
    # Check if the address is 42 characters long and starts with '0x'
    if len(address) == 42 and address.startswith('0x'):
        # Check if the rest of the address contains only hexadecimal characters
        return re.fullmatch(r'0x[0-9a-fA-F]{40}', address) is not None
    return False

def is_valid_eth_private_key(key):
    import re
    if not isinstance(key, str):
        return False

    # Check if the key is 64 characters long and contains only hexadecimal characters
    return len(key) == 64 and re.fullmatch(r'[0-9a-fA-F]{64}', key) is not None

def to_checksum_address(address):
    from web3 import Web3
    return Web3.to_checksum_address(address)

def get_provider(chain=CHAIN_ID_ETH):
    import os
    provider = os.environ.get("UNISWAP_PROVIDER_ETH")
    if chain == CHAIN_ID_OP:
        return os.environ.get("UNISWAP_PROVIDER_OP")
    elif chain == CHAIN_ID_BNB:
        return os.environ.get("UNISWAP_PROVIDER_BNB")
    else:
        return provider
