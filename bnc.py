from binance import Client
from binance.enums import SIDE_BUY, ORDER_TYPE_MARKET
from dotenv import load_dotenv
import time
import datetime
import os
import logging

load_dotenv()
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Binance Client
api_key = os.environ.get('BINANCE_API_KEY')
api_secret = os.environ.get('BINANCE_API_SECRET')
testnet = os.environ.get('IS_TESTNET', True)
client = Client(api_key, api_secret, testnet=testnet)



def get_user_input():
    # print("test", testnet, client.API_URL, client.API_TESTNET_URL)
    symbol = input("Enter the symbol (e.g., 'BTCUSDT'): ")
    quantity = float(input("Enter total quantity to trade: "))
    duration = float(input("Enter TWAP duration in hours: "))
    return symbol, quantity, duration



def execute_twap_order(symbol, total_quantity, duration_hours, interval_seconds=60):
    end_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)
    total_intervals = duration_hours * 3600 / interval_seconds
    order_quantity = total_quantity / total_intervals

    while datetime.datetime.now() < end_time:
        try:
            # Execute market order
            order = client.create_order(
                symbol=symbol,
                side=SIDE_BUY,
                type=ORDER_TYPE_MARKET,
                quantity=order_quantity
            )
            logging.info(f"Order executed: {order}")
        except Exception as e:
            logging.error(f"Error executing order: {e}")

        time.sleep(interval_seconds)


def main():
    symbol, quantity, duration = get_user_input()
    execute_twap_order(symbol, quantity, duration)

if __name__ == "__main__":
    main()
