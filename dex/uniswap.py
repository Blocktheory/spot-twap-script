from uniswap import Uniswap
from dotenv import load_dotenv
import time
import datetime
import os
import logging

load_dotenv()
# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Uniswap Client
key = os.environ.get('UNISWAP_PUBLIC_KEY')
secret = os.environ.get('UNISWAP_PRIVATE_KEY')
provider = os.environ.get('UNISWAP_PROVIDER')
version = 2
uniswap = Uniswap(address=key, private_key=secret,
                  version=version, provider=provider)

# Some token addresses we'll be using later in this guide
eth = "0x0000000000000000000000000000000000000000"
bat = "0x0D8775F648430679A709E98d2b0Cb6250d2887EF"
usdc = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
dai = "0x6B175474E89094C44Da98b954EedeAC495271d0F"

def make_trade():
    # Make a trade by specifying the quantity of the input token you wish to sell
    uniswap.make_trade(eth, bat, 1*10**18)  # sell 1 ETH for BAT
    uniswap.make_trade(bat, eth, 1*10**18)  # sell 1 BAT for ETH
    uniswap.make_trade(bat, dai, 1*10**18)  # sell 1 BAT for DAI
    uniswap.make_trade(eth, bat, 1*10**18, "0x06e70f295B6337c213DDe82D13cc198027687A7B")  # sell 1 ETH for BAT, and send the BAT to the provided address
    uniswap.make_trade(dai, usdc, 1*10**18, fee=500)    # sell 1 DAI for USDC using the 0.05% fee pool (v3 only)

def make_trade_output():
    # Make a trade by specifying the quantity of the output token you wish to buy
    uniswap.make_trade_output(eth, bat, 1*10**18)  # buy ETH for 1 BAT
    uniswap.make_trade_output(bat, eth, 1*10**18)  # buy BAT for 1 ETH
    uniswap.make_trade_output(bat, dai, 1*10**18, "0x06e70f295B6337c213DDe82D13cc198027687A7B")  # buy BAT for 1 DAI, and send the BAT to the provided address
    uniswap.make_trade_output(dai, usdc, 1*10**8, fee=500)     # buy USDC for 1 DAI using the 0.05% fee pool (v3 only)

def get_prices_list():
    prices = uniswap.get_price_input(eth, dai, 10**18)
    print("prices: ", prices)
    return prices


def check_balance():
    ethBal = uniswap.get_eth_balance()
    print("ethBal: ", ethBal)
    return ethBal


