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

pub_key = os.environ.get("JUPITER_PUBLIC_KEY")
secret = os.environ.get("JUPITER_PRIVATE_KEY")
provider = os.environ.get("JUPITER_PROVIDER_SOL")
# Define the API endpoint for quote
quote_url = "https://quote-api.jup.ag/v6/quote"
swap_url = "https://quote-api.jup.ag/v6/swap"


def execute(token_pair_symbol, trade_type, total_quantity, duration_hours, interval_minutes=1, address=None, key=None, chain=None):
    
    private_key = secret
    if key is not None and key != "":
        private_key = key
    wallet = Keypair.from_bytes(base58.b58decode(private_key))
    public_key = wallet.pubkey()
    public_key_str = str(public_key)

    slippage = 1000  # 1000 1% slippage
    end_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)
    interval_seconds = interval_minutes * 60
    quantity = total_quantity*10**token1_decimals

    token1_details, token2_details = get_token_details(
        token_pair_symbol, chain)
    if address == None:
        address = pub_key
    token1_address = token1_details["address"].lower()
    token1_decimals = token2_details["decimals"]
    token2_address = token2_details["address"].lower()
    print(token1_details, token2_details)
    while datetime.datetime.now() < end_time:
        try:
            if trade_type.lower() == "buy":
                # Define the parameters for the swap
                params = {
                    "inputMint": token1_address,  
                    "outputMint": token2_address,  
                    "amount": quantity,  
                    "slippageBps": slippage
                }
                try:
                    quote_response = requests.get(quote_url, params=params)
                    # This will raise an HTTPError if the response was unsuccessful
                    quote_response.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    print(f"HTTP error occurred: {err}")
                except Exception as err:
                    print(f"Other error occurred: {err}")
                else:
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

    # Create a Solana client
    solana_client = Client(provider)

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
