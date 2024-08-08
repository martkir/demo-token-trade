from web3 import Web3


def create_wallet():
    web3 = Web3()
    account = web3.eth.account.create()
    private_key = account.privateKey.hex()
    address = account.address
    return address, private_key


if __name__ == "__main__":
    address, private_key = create_wallet()
    print("Address: ", address)
    print("Private key: ", private_key)
