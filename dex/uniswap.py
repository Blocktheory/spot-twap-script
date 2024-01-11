from uniswap import Uniswap
from dotenv import load_dotenv
from utils import get_provider, get_token_details, to_checksum_address

import time
import datetime
import os
import logging

load_dotenv()
# Setup logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Uniswap Client
pub_key = os.environ.get("UNISWAP_PUBLIC_KEY")
secret = os.environ.get("UNISWAP_PRIVATE_KEY")
version = 2
uniswap = Uniswap(address=pub_key, private_key=secret,
                  version=version, provider=get_provider())

def execute(token_pair_symbol, trade_type, total_quantity, duration_hours, interval_minutes=1, address=None, key=None, chain=None):
    provider = get_provider(chain)
    uniswap.provider = provider
    if address == None or address == "":
        address = pub_key
    if key != None:
        uniswap.private_key = key
        uniswap.address = address
    token1_details, token2_details = get_token_details(
        token_pair_symbol, chain)
    if not token1_details or not token1_details["address"]:
        print("Enter valid from token symbol")
        return
    if not token2_details or not token2_details["address"]:
        print("Enter valid to token symbol")
        return
    token1_address = to_checksum_address(token1_details["address"])
    token1_decimals = token2_details["decimals"]
    token2_address = to_checksum_address(token2_details["address"])
    end_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)
    interval_seconds = interval_minutes * 60
    quantity = int(total_quantity*10**token1_decimals)
    address = to_checksum_address(address)
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
