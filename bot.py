import time
import json
from web3 import Web3
from checkpoint import save_checkpoint, load_checkpoint
import config

# Web3 connection
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
account = w3.eth.account.from_key(config.PRIVATE_KEY)

# Load ABI
with open("router_abi.json") as f:
    abi = json.load(f)

router = w3.eth.contract(address=w3.to_checksum_address(config.ROUTER_ADDRESS), abi=abi)

def swap_token(amount, token_in, token_out):
    amount_in = w3.to_wei(amount, "ether")
    amount_out_min = int(amount_in * 0.95)
    path = [w3.to_checksum_address(token_in), w3.to_checksum_address(token_out)]
    deadline = int(time.time()) + 1800

    tx = router.functions.swapExactTokensForTokens(
        amount_in,
        amount_out_min,
        path,
        config.WALLET_ADDRESS,
        deadline
    ).build_transaction({
        "from": config.WALLET_ADDRESS,
        "nonce": w3.eth.get_transaction_count(config.WALLET_ADDRESS),
        "gas": 200000,
        "maxFeePerGas": w3.to_wei("2", "gwei"),
        "maxPriorityFeePerGas": w3.to_wei("1", "gwei"),
        "chainId": 9090
    })

    signed_tx = w3.eth.account.sign_transaction(tx, config.PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"🔁 Swap sent: {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("✅ Confirmed!" if receipt.status == 1 else "❌ Failed.")

# Main loop
start = load_checkpoint()
for i in range(start, 100):
    try:
        print(f"\n=== SWAP #{i + 1} ===")
        swap_token(0.01, config.TOKEN_IN, config.TOKEN_OUT)
        save_checkpoint(i + 1)
        time.sleep(40)
    except Exception as e:
        print(f"❌ Error at swap #{i + 1}: {e}")
        break
