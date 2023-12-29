from binance import Client
from dotenv import load_dotenv
import time
import datetime
import os
import logging

load_dotenv()
# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Binance Client
api_key = os.environ.get('BINANCE_API_KEY')
api_secret = os.environ.get('BINANCE_API_SECRET')
testnet = os.environ.get('IS_TESTNET', True)
client = Client(api_key, api_secret, testnet=testnet)

def execute_twap_order(token_pair_symbol, trade_type, total_quantity, duration_hours, interval_minutes=1):
    end_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)
    interval_seconds = interval_minutes * 60
    while datetime.datetime.now() < end_time:
        try:
            order = client.create_order(
                symbol=token_pair_symbol,
                side=Client.SIDE_BUY if trade_type.lower() == "buy" else Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=total_quantity
            )
            print(f"Order executed: {order}")
        except Exception as e:
            print(f"Error executing order: {e}")
        print(f"waiting {interval_minutes} minutes for next order...")
        time.sleep(interval_seconds)

# Extra functions to get meta data if required
def get_prices_list():
    prices = client.get_all_tickers()
    return prices

def check_balance(asset):
    return client.get_asset_balance(asset=asset)

def get_open_orders(token_pair_symbol):
    return client.get_open_orders(symbol=token_pair_symbol)
