import time
import datetime
import os
from dotenv import load_dotenv
from pymexc import spot

load_dotenv()
key = os.environ.get('MEXC_API_KEY')
secret = os.environ.get('MEXC_API_SECRET')

client = spot.HTTP(api_key=key, api_secret=secret)

def execute(symbol, trade_type, order_quantity, duration_hours, interval_minutes=1):
    end_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)
    interval_seconds = interval_minutes * 60
    while datetime.datetime.now() < end_time:
        try:
            # Execute market order
            order = client.new_order(
                symbol=symbol,
                side="BUY" if trade_type.lower() == "buy" else "SELL",
                order_type="MARKET",
                quantity=order_quantity,
            )
            print(f"Order executed: {order}")
        except Exception as e:
            print("Error executing order", e)
        print(f"waiting {interval_minutes} minutes for next order...")
        time.sleep(interval_seconds)
