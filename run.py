import time
from web3 import Web3
import json
import os
from dotenv import load_dotenv


load_dotenv()


if __name__ == "__main__":
    wallet_address = os.environ.get("ADDRESS")
    private_key = os.environ.get("PRIVATE_KEY")
    node_api_key = os.environ.get("NODE_API_KEY")
    node_endpoint = os.environ.get("NODE_ENDPOINT")
    repo_dir = os.getcwd()

    in_token_address = "0x779877A7B0D9E8603169DdbD7836e478b4624789"  # ChainLink
    router_address = "0xC532a74256D3Db42D0Bf7a0400fEFDbad7694008"

    if any([
        node_api_key is None,
        private_key is None,
        node_api_key is None,
        node_endpoint is None,
    ]):
        raise Exception("One or more environment variables are missing. See 'README.md'.")

    # Connection to Sepolia testnet through QuickNode
    node_url = f"{node_endpoint}/{node_api_key}"
    web3 = Web3(Web3.HTTPProvider(node_url))

    # Verify connection
    assert web3.isConnected(), "Failed to connect to Ethereum network"

    # ABI for interacting with the Uniswap Router
    router_path = f"{repo_dir}/utils/data/abis/sepolia_uniswap_router.json"    
    router_abi = json.load(open(router_path))

    # Initialize the Uniswap Router contract
    router_contract = web3.eth.contract(address=router_address, abi=router_abi)  # type: ignore
    out_token = web3.toChecksumAddress("0x7b79995e5f793A07Bc00c21412e50Ecae098E7f9")  # Wrapped ETH
    in_token = web3.toChecksumAddress(in_token_address)
    path = [out_token, in_token]

    gas_price = web3.toWei('10', 'gwei')
    amount_in_wei = web3.toWei(0.001, 'ether')  # Amount of ETH to swap
    amount_out_min = 0  # Minimum amount of tokens to receive (set to 0 for simplicity)
    deadline = int(time.time()) + 10 * 60  # 10 minutes from now

    transaction = router_contract.functions.swapExactETHForTokens(
        amount_out_min,
        path,
        wallet_address,
        # Explain what 'deadline' does
        deadline
    ).buildTransaction({
        'from': wallet_address,
        'value': amount_in_wei,
        # The 'gas' parameter sets the maximum amount of gas units that the transaction can consume.
        # If the gas limit is too low, the transaction might fail due to running out of gas. Eexcess gas will be refunded.
        # If multi-swap gas limit needs to be higher
        'gas': 2000000,
        # The 'gasPrice' parameter sets the price per gas unit in wei. Higher gas prices can expedite the transaction processing as miners prioritize transactions with higher gas prices.
        # Lower gas prices might result in slower transaction processing.
        # If 'gasPrice' is not high enough the transaction might not be included in the current block - Instead
        # remain in the mempool and be picked up in a later block.
        'gasPrice': gas_price,
        # The 'nonce' parameter is a unique number that indicates the number of transactions sent from the address.
        # It is used to prevent replay attacks and ensure the proper ordering of transactions.
        'nonce': web3.eth.getTransactionCount(wallet_address)
    })

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    # Send the transaction
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    tx_hash_decoded = tx_receipt.transactionHash.hex()
    print(f"Transaction successful with hash: {tx_hash_decoded}")
    print(f"Etherscan: https://sepolia.etherscan.io/tx/{tx_hash_decoded}")
