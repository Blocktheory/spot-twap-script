from utils import calculate_order_quantity, get_user_input, sanity_check

def main():
    dex, symbol, trade_type, quantity, duration, interval, address, chain, key = get_user_input()
    order_quantity = calculate_order_quantity(
        quantity, duration, interval)
    print("placed order quantity ", order_quantity)
    is_valid = sanity_check(dex, symbol, trade_type, order_quantity,
                            float(duration),  float(interval), address, chain, key)
    if not is_valid:
        print("sanity check failed")
        return
    if dex.lower() == "binance":
        from cex import bnc
        bnc.execute(
            symbol, trade_type, order_quantity, float(duration), float(interval))
    elif dex.lower() == "gate":
        from cex import gate
        gate.execute(symbol, trade_type, order_quantity, float(duration), float(interval))
    elif dex.lower() == "mexc":
        from cex.mexc import mexc
        mexc.execute(symbol, trade_type, order_quantity, float(duration), float(interval))
    elif dex.lower() == "uniswap":
        from dex import uniswap
        uniswap.execute(symbol, trade_type, order_quantity, float(
            duration), float(interval), address, key, chain)
    elif dex.lower() == "jupiter":
        from dex import jup
        jup.execute(symbol, trade_type, order_quantity, float(
            duration), float(interval), address, key, chain)

if __name__ == "__main__":
    main()
