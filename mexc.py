import time
import datetime
import os
from dotenv import load_dotenv
from pymexc import spot

load_dotenv()

spot_client = spot.HTTP(api_key = os.getenv("MEXC_API_KEY"), api_secret = os.getenv("MEXC_API_SECRET"))

def execute(symbol, total_quantity, duration_hours, interval_seconds=60):
    end_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)
    total_intervals = duration_hours * 3600 / interval_seconds
    order_quantity = total_quantity / total_intervals
    # print("order_quantity", order_quantity) 
    # print(order)
    while datetime.datetime.now() < end_time:   
        try:
            # Execute market order
            order_result = spot_client.new_order(
                symbol=symbol,
                side="BUY",
                order_type="MARKET",
                quantity=order_quantity,
                # timestamp=int(time.time())
            )
            print("Order executed", order_result)
        except Exception as e:
            print("Error executing order", e)

        time.sleep(interval_seconds)