from utils import calculate_order_quantity, get_user_input, sanity_check

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
    if dex.lower() == "binance":
        import bnc
        bnc.execute_twap_order(
            symbol, trade_type, order_quantity, float(duration), float(interval))
    elif dex.lower() == "gate":
        import gate
        gate.execute(symbol, trade_type, order_quantity, float(duration), float(interval))
    elif dex.lower() == "mexc":
        import mexc
        mexc.execute(symbol, trade_type, order_quantity, float(duration), float(interval))

if __name__ == "__main__":
    main()