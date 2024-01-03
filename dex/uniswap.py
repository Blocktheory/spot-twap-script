from uniswap import Uniswap
from dotenv import load_dotenv
from utils import get_token_details

import time
import datetime
import os
import logging

load_dotenv()
# Setup logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Uniswap Client
key = os.environ.get("UNISWAP_PUBLIC_KEY")
secret = os.environ.get("UNISWAP_PRIVATE_KEY")
provider = os.environ.get("UNISWAP_PROVIDER")
version = 2
uniswap = Uniswap(address=key, private_key=secret,
                  version=version, provider=provider)

def execute(token_pair_symbol, trade_type, total_quantity, duration_hours, interval_minutes=1, address=None):
    token1_details, token2_details = get_token_details(token_pair_symbol)
    if address == None:
        address = key
    token1_address = token1_details["address"].lower()
    token1_decimals = token2_details["decimals"]
    token2_address = token2_details["address"].lower()
    end_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)
    interval_seconds = interval_minutes * 60
    quantity = total_quantity*10**token1_decimals
    while datetime.datetime.now() < end_time:
        try:
            if trade_type.lower() == "buy":
                order = uniswap.make_trade_output(
                    token1_address, token2_address, quantity, address)
                print(f"Order executed: {order}")
            else:
                order = uniswap.make_trade(token1_address, token2_address,
                                           quantity, address)
                print(f"Order executed: {order}")
        except Exception as e:
            print(f"Error executing order: {e}")
        if datetime.datetime.now() < end_time:
            print(f"waiting {interval_minutes} minutes for next order...")
            time.sleep(interval_seconds)
    # uniswap.make_trade(dai, usdc, 1*10**18, fee=500)

def get_prices_list():
    token1_details, token2_details = get_token_details("eth_dai")
    prices = uniswap.get_price_input(
        token1_details.address, token2_details.address, 10**18)
    print("prices: ", prices)
    return prices


def check_balance():
    ethBal = uniswap.get_eth_balance()
    print("ethBal: ", ethBal)
    return ethBal
