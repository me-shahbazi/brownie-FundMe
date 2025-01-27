from brownie import network, accounts
from web3 import Web3


def main():
    print(network.show_active()) # type: ignore
    if "ganache" in str(network.show_active()): # type: ignore
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

        # Check connection
        if w3.is_connected():
            print("Connected to the blockchain")

            # Get the current block number
            current_block = w3.eth.block_number
            print(f"Current Block Number: {current_block}")
        else:
            print("Failed to connect to the blockchain")
        
        # Replace with the address you want to check
        _Account = accounts.add("0x2a590abaea3a68e4029d9096fbdc38ebab90dde6ba2afea7d3efe4feb1190650")

        # Get the nonce for the specified address
        nonce = w3.eth.get_transaction_count(_Account.address)
        
        print(f"Nonce for address {str(_Account)}: {nonce}")


    x=2
    print(f"\n{x} Eth is {Web3.to_wei(x,"ether")} Wei")