from dotenv import load_dotenv
# import logging

load_dotenv()
# # Setup logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_user_input():
    dex = input("Choose your exchange platform. binance or gate: ")
    symbol = input("Enter the trading pair symbol (e.g., 'BNBUSDT'): ")
    trade_type = input("Specify the trade type. buy or sell: ")
    quantity = input("Enter the quantity to trade (units): ")
    duration = input("Specify the duration of the order in hours: ")
    interval = input("Enter the interval for each TWAP in minutes: ")
    return dex, symbol, trade_type, quantity, duration, interval

def calculate_order_quantity(quantity, duration_hours, interval):
    try:
        quantity = float(quantity)
        duration_hours = float(duration_hours)
        interval = float(interval)
    except:
        return 0
    if interval <= 0:
        return 0
    interval_seconds = interval * 60  # converting to seconds
    total_intervals = duration_hours * 3600 / interval_seconds
    return round(quantity / total_intervals, 2)


def sanity_check(dex, token_pair_symbol, trade_type, order_quantity, duration_hours, interval_minutes):
    if not dex or dex.lower() not in ["gate", "binance", "mexc"]:
        print("Enter valid dex (gate, binance, mexc)")
        return False
    if not token_pair_symbol:
        print("Enter valid token pair")
        return False
    if not order_quantity or order_quantity <= 0:
        print("Enter quantity is less than 0.01 for each interval, make sure to increase the quantity")
        return False
    if not interval_minutes or interval_minutes < 0.1:
        print("Enter valid interval minutes, make sure its greater than 0.1")
        return False
    if not duration_hours or duration_hours < 0.1:
        print("Enter valid duration in hours, make sure its greater than 0.1")
        return False
    if not trade_type or trade_type.lower() not in ["buy", "sell"]:
        print("Enter valid trade type buy or sell")
        return False
    return True

def main():
    dex, symbol, trade_type, quantity, duration, interval = get_user_input()
    order_quantity = calculate_order_quantity(
        quantity, duration, interval)
    print("placed order quantity ", order_quantity)
    is_valid = sanity_check(dex, symbol, trade_type, order_quantity,
                            float(duration),  float(interval))
    if not is_valid:
        print("sanity check failed")
        return
    if dex == "binance":
        import bnc
        bnc.execute_twap_order(
            symbol, trade_type, order_quantity, float(duration), float(interval))
    elif dex == "gate":
        import gate
        gate.execute(symbol, order_quantity, float(duration))


if __name__ == "__main__":
    main()
