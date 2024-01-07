import base58
import os
import requests
import json
import base64
import solana
from dotenv import load_dotenv
from solders.transaction import Transaction, VersionedTransaction
from solana.rpc.api import Client
from solana.rpc.core import RPCException
from solders.keypair import Keypair
from solders import message
from solana.rpc.types import TxOpts
from solders.system_program import TransferParams
from solders.pubkey import Pubkey

import time
import datetime
import os
import logging

from utils import get_token_details

## WIP - Do not test

load_dotenv()
# Setup logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

key = os.environ.get("JUPITER_PUBLIC_KEY")
secret = os.environ.get("JUPITER_PRIVATE_KEY")
# Define the API endpoint for quote
quote_url = "https://quote-api.jup.ag/v6/quote"
swap_url = "https://quote-api.jup.ag/v6/swap"


def execute(token_pair_symbol, trade_type, total_quantity, duration_hours, interval_minutes=1, address=None):
    # to be made dynamic
    slippage = 1000  # 1000 1% slippage
    token1_details, token2_details = get_token_details(token_pair_symbol)
    if address == None:
        address = key
    token1_address = token1_details["address"].lower()
    token1_decimals = token2_details["decimals"]
    token2_address = token2_details["address"].lower()
    end_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)
    interval_seconds = interval_minutes * 60
    quantity = total_quantity*10**token1_decimals
    while datetime.datetime.now() < end_time:
        try:
            if trade_type.lower() == "buy":
                # Need to add buy function here
                # Define the parameters for the swap
                params = {
                    "inputMint": token1_address,  # SOL So11111111111111111111111111111111111111112
                    "outputMint": token2_address,  # USDC 7iT1GRYYhEop2nV1dyCwK2MGyLmPHq47WhPGSwiqcUg5
                    "amount": quantity,  # 10000000 0.01 SOL
                    "slippageBps": slippage  # 1000 1% slippage
                }
                # Send a GET request to the API
                try:
                    quote_response = requests.get(quote_url, params=params)
                    # This will raise an HTTPError if the response was unsuccessful
                    quote_response.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    print(f"HTTP error occurred: {err}")
                except Exception as err:
                    print(f"Other error occurred: {err}")
                else:
                    # Parse the response
                    quote_data = quote_response.json()
                return
            else:
                # Need to add sell function here
                return
        except Exception as e:
            print(f"Error executing order: {e}")
        if datetime.datetime.now() < end_time:
            print(f"waiting {interval_minutes} minutes for next order...")
            time.sleep(interval_seconds)
            

    private_key = secret  # Replace with your private key
    wallet = Keypair.from_bytes(base58.b58decode(private_key))
    public_key = wallet.pubkey()
    # Convert the public key to a string
    public_key_str = str(public_key)

    # Define the body for the swap
    body = {
        "quoteResponse": quote_data,  # Use the response from the previous /quote API call
        "userPublicKey": public_key_str,  # Replace with your public key
        "wrapAndUnwrapSol": True,  # Auto wrap and unwrap SOL
        # "feeAccount": "fee_account_public_key"  # Optional: Use if you want to charge a fee. feeBps must have been passed in /quote API.
    }

    # Send a POST request to the API
    swap_response = requests.post(
        swap_url, headers={'Content-Type': 'application/json'}, data=json.dumps(body))

    # Get the serialized transaction
    serialized_transaction = swap_response.json()["swapTransaction"]

    if serialized_transaction is None:
        print("No 'swapTransaction' field in the response")

    helis_api_key = os.getenv("HELIUS_API_KEY")
    # Create a Solana client
    solana_client = Client(
        f"https://mainnet.helius-rpc.com/?api-key={helis_api_key}")

    # Create a transaction
    # Decode the base64 string
    try:
        raw_txn = VersionedTransaction.from_bytes(
            base64.b64decode(serialized_transaction))
    except Exception as e:
        print("Error decoding base64:", e)

    # Define transaction options
    # recent_blockhash = solana_client.get_latest_blockhash()
    # blockhash_str = recent_blockhash.value.blockhash

    try:
        simulation_result = simulate_transaction(
            solana_client, raw_txn, wallet)
        print("Simulation result:", simulation_result)
        simulate_result = False
        if simulation_result.value.err is None:
            simulate_result = True
            print("Simulation successful, transaction is likely to succeed.")
            # return "Simulation successful, transaction is likely to succeed."
        else:
            print("Simulation failed:", simulation_result.value.err)
            # return "Simulation failed"
        if simulate_result:
            send_tx = send_transaction(solana_client, raw_txn, wallet)
            print("send tx successful", send_tx)
            return send_tx
    except Exception as e:
        print("Simulation error:", e)
        return "Simulation error"


def simulate_transaction(client, raw_txn, wallet):
    try:
        # Sign the transaction
        signature = wallet.sign_message(
            message.to_bytes_versioned(raw_txn.message))
        simulated_txn = VersionedTransaction.populate(
            raw_txn.message, [signature])

        # Simulate the transaction
        simulate_Tx = client.simulate_transaction(
            simulated_txn,
            commitment="confirmed",
        )
        return simulate_Tx
    except Exception as e:
        return e


def send_transaction(client, raw_txn, wallet, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Sign the transaction
            signature = wallet.sign_message(
                message.to_bytes_versioned(raw_txn.message))
            signed_txn = VersionedTransaction.populate(
                raw_txn.message, [signature])

            # Send the transaction
            result = client.send_transaction(
                signed_txn,
                opts=TxOpts(skip_preflight=False,
                            preflight_commitment="confirmed"),
            )
            return result.value
        except RPCException as err:
            err_str = str(err)
            if 'blockhash not found' in err_str:
                print(
                    f"Blockhash invalid, retrying... (Attempt {attempt + 1} of {max_retries})")
            elif 'SlippageToleranceExceeded' in err_str:
                print(
                    "Slippage tolerance exceeded. Please update your slippage tolerance and try again.")
                return "Slippage tolerance exceeded. Please update your slippage tolerance and try again."
            else:
                return err
        except Exception as e:
            return e
    return ("Failed to send transaction after several attempts")
