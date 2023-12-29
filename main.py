from dotenv import load_dotenv
# import logging

load_dotenv()
# # Setup logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_user_input():
    dex = input("Choose your dex (binance/gate): ")
    symbol = input("Enter the symbol (e.g., 'BTCUSDT'): ")
    quantity = float(input("Enter total quantity to trade: "))
    duration = float(input("Enter TWAP duration in hours: "))
    return dex, symbol, quantity, duration


def main():
    dex, symbol, quantity, duration = get_user_input()
    if dex == "binance":
        import bnc
        bnc.execute_twap_order(symbol, quantity, duration)
    elif dex == "gate":
        import gate
        gate.execute(symbol, quantity, duration)
        

if __name__ == "__main__":
    main()