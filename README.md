# demo-token-trade
A minimal example of how to programmatically buy an ERC20 token on Ethereum using Python.

# Running the script

```
cd $REPO_DIR
python run.py
```

The `run.py` script will buy token `0x779877A7B0D9E8603169DdbD7836e478b4624789` (ChainLink) using **Uniswap** on the **Ethereum Sepolia Testnet** network.

Before running the script make sure to go over the **setup steps**.

# Setup

## Python Enviroment and Installation

```
cd $REPO_DIR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

`$REPO_DIR` is the directory you cloned this repository to.

## Environment Variables

Create an `.env` file in the repository like so:

```
cd $REPO_DIR
touch .env
```

Add `ADDRESS`, `PRIVATE_KEY`, `NODE_API_KEY` and `NODE_ENDPOINT` variables to the `.env` file.

```
ADDRESS="YOUR_ADDRESS"
PRIVATE_KEY="YOUR_PRIVATE_KEY"
NODE_API_KEY="YOUR_NODE_API_KEY"
NODE_ENDPOINT="YOUR_NODE_ENDPOINT"
```

To **create an address and private key** use:

```
cd $REPO_DIR
python -m utils.create_wallet
```

To run `run.py` you will need to connect to a node provider by providing an endpoint and API key.

Popular **node providers** are:

- https://www.quicknode.com
- https://www.alchemy.com/
- https://www.infura.io/

The code in `run.py` assumes it is executed on the Ethereum **Sepolia Testnet** netowrk.

Make sure to create an endpoint and API key for the **Ethereum Sepolia Testnet** network.

## Funding your Wallet

You can use a **faucet** to fund your wallet for free.

This is the faucet I used: https://cloud.google.com/application/web3/faucet/ethereum/sepolia

