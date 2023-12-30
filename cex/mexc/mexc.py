import time
import datetime
import os
from dotenv import load_dotenv
from . import mexc_spot_v3

load_dotenv()
hosts = "https://api.mexc.com"
key = os.environ.get('MEXC_API_KEY')
secret = os.environ.get('MEXC_API_SECRET')

def execute(symbol, trade_type, order_quantity, duration_hours, interval_minutes=1):
    end_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)
    interval_seconds = interval_minutes * 60
    while datetime.datetime.now() < end_time:
        try:
            # Execute market order
            trade = mexc_spot_v3.mexc_trade(
                mexc_key=key, mexc_secret=secret, mexc_hosts=hosts)
            params = {
                "symbol": symbol,
                "side": "BUY" if trade_type.lower() == "buy" else "SELL",
                "type": "MARKET",
                "quantity": order_quantity,
            }
            response = trade.post_order(params)
            print(f"Order executed: {response}")
        except Exception as e:
            print("Error executing order", e)
        if datetime.datetime.now() < end_time:
            print(f"waiting {interval_minutes} minutes for next order...")
            time.sleep(interval_seconds)

# Extra functions to get account meta data if required
def get_default_symbols():
    market = mexc_spot_v3.mexc_market(
        mexc_hosts=hosts)
    symbols = market.get_defaultSymbols()
    print("default symbols: ", symbols)
    return symbols

def get_prices_list():
    capital = mexc_spot_v3.mexc_capital(
        mexc_key=key, mexc_secret=secret, mexc_hosts=hosts)
    prices = capital.get_coinlist()
    print("prices: ", prices)
    return prices

def check_balance(asset):
    account = mexc_spot_v3.mexc_account(
        mexc_key=key, mexc_secret=secret, mexc_hosts=hosts)
    bal = account.get_account_info()
    print("bal: ", bal)
    return bal

def get_rebate_records():
    margin = mexc_spot_v3.mexc_rebate(
        mexc_key=key, mexc_secret=secret, mexc_hosts=hosts)
    rebate_record = margin.get_rebate_detail()
    print("rebate_record: ", rebate_record)
    return rebate_record
