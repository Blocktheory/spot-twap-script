import gate_api
import time
import datetime
import os
from gate_api.exceptions import ApiException, GateApiException
from dotenv import load_dotenv
import logging

load_dotenv()

configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4",
    key = os.getenv("GATE_API_KEY"),
    secret = os.getenv("GATE_API_SECRET")
)

api_client = gate_api.ApiClient(configuration)
# Create an instance of the API class
api_instance = gate_api.SpotApi(api_client)

def execute(symbol, total_quantity, duration_hours, interval_seconds=60):
    end_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)
    total_intervals = duration_hours * 3600 / interval_seconds
    order_quantity = total_quantity / total_intervals
    # print("order_quantity", order_quantity) 
    order = gate_api.Order(type="market", currency_pair=symbol, side="buy", amount=str(order_quantity), time_in_force="ioc")
    # print(order)
    while datetime.datetime.now() < end_time:   
        try:
            # Execute market order
            order_result = api_instance.create_order(
                order=order
            )
            print("Order executed", order_result)
        except Exception as e:
            print("Error executing order", e)

        time.sleep(interval_seconds)
