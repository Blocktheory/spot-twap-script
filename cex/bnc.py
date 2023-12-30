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
key = os.environ.get('BINANCE_API_KEY')
secret = os.environ.get('BINANCE_API_SECRET')

client = Client(key, secret, testnet=False)

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
        if datetime.datetime.now() < end_time:
            print(f"waiting {interval_minutes} minutes for next order...")
            time.sleep(interval_seconds)

# Extra functions to get account meta data if required
def get_prices_list():
    prices = client.get_all_tickers()
    print("prices: ", prices)
    return prices

def check_balance(asset):
    bal = client.get_asset_balance(asset=asset)
    print("bal: ", bal)
    return bal

def get_open_orders(token_pair_symbol):
    open_orders = client.get_open_orders(symbol=token_pair_symbol)
    print("open_orders: ", open_orders)
    return open_orders
