import gate_api
import time
import datetime
import os
from gate_api.exceptions import ApiException, GateApiException
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GATE_API_KEY")
secret = os.getenv("GATE_API_SECRET")

configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4",
    key = key,
    secret=secret
)

api_client = gate_api.ApiClient(configuration)
# Create an instance of the API class
api_instance = gate_api.SpotApi(api_client)

def execute(symbol, trade_type, order_quantity, duration_hours, interval_minutes):
    end_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)
    interval_seconds = interval_minutes * 60
    order = gate_api.Order(type="market", currency_pair=symbol, side="buy" if trade_type.lower() == "buy" else "sell", amount=str(order_quantity), time_in_force="ioc")
    while datetime.datetime.now() < end_time:   
        try:
            # Execute market order
            order_result = api_instance.create_order(
                order=order
            )
            print("Order executed", order_result)
        except Exception as e:
            print("Error executing order", e)
        print(f"waiting {interval_minutes} minutes for next order...")
        time.sleep(interval_seconds)
