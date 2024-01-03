
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

def sanity_check(dex, token_pair_symbol, trade_type, order_quantity, duration_hours, interval_minutes):
    if not dex or dex.lower() not in ["gate", "binance", "mexc", "uniswap"]:
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
    return True

def get_user_input():
    dex = input("Choose your exchange platform binance or gate or mexc or uniswap: ")
    symbol = input("Enter the trading pair symbol (e.g., 'BNBUSDT'): ")
    trade_type = input("Specify the trade type to buy or sell: ")
    quantity = input("Enter the quantity to trade (units): ")
    duration = input("Specify the duration of the order in hours: ")
    interval = input("Enter the interval for each TWAP in minutes: ")
    address = None
    if dex == "uniswap":
        address = input("Enter the address you want to send (optional): ")
    return dex, symbol, trade_type, quantity, duration, interval, address

def load_tokens(file_path):
    import json
    with open(file_path, "r") as file:
        return json.load(file)

def fetch_token_data():
    return load_tokens("./constants/tokens.json")


def get_token_details(token_combination):
    tokens_data = fetch_token_data()
    if "_" in token_combination:
        # Split the input to get individual tokens
        token1, token2 = token_combination.split("_")
    else:
        # Handle it as a single token
        token1 = token_combination
        token2 = None

    # Define a helper function to find a token in the tokens data
    def find_token(token, tokens_data):
        for token_data in tokens_data:
            if token.lower() in [token_data["symbol"].lower(), token_data["address"].lower()]:
                return token_data
        return None

    # Find each token
    token1_details = find_token(token1, tokens_data)
    token2_details = find_token(token2, tokens_data)

    return token1_details, token2_details
