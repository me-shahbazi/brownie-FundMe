from brownie import accounts, config, network
from brownie import FundMe # type: ignore
from brownie import MockV3Aggregator # type: ignore
from scripts.Common import myAccount
from scripts.Common import _ETH, _Gwei, _Wei

currentNetwork = None

def initialize_network():
    """Initialize the network and ensure it's set globally."""
    global currentNetwork
    currentNetwork = network.show_active()  # type: ignore # Get the active network
    if not currentNetwork:
        raise ValueError("No active network. Please check your Brownie configuration.")
    print("Current Network initialized: ", currentNetwork , type(currentNetwork))
    return currentNetwork

def selectAccount():
    global currentNetwork
    
    _Account = myAccount(currentNetwork).autoAccount()
    
    print("Using Account: ", _Account)
    return _Account

def deployContracts(_Account):
    global currentNetwork
    
    if currentNetwork == "ganacheUI":
        mockAddress = MockV3Aggregator.deploy(18,3000*10**8,{"from": _Account})
        depContract = FundMe.deploy(mockAddress,{"from": _Account}, publish_source=False) # or mockAddress.address
    elif currentNetwork == "development" : 
        mockAddress = MockV3Aggregator.deploy(18,3000*10**8,{"from": _Account})
        depContract = FundMe.deploy(mockAddress,{"from": _Account}, publish_source=False) # or mockAddress.address
    else: # real Network
        depContract = FundMe.deploy(config["networks"][currentNetwork]["ethusd"],{"from": _Account}, publish_source=False)
    return depContract

def fund(account, contract, value: int):
    fundTxn = contract.fund({"from": account, "value": value})
    fundTxn.wait(1) # Wait One Block before Continue
    return fundTxn

def withDraw(_Account, depContract):
    Txn = depContract.withdrawFunds({"from": _Account})
    Txn.wait(1) # Wait One Block before Continue
    return Txn
    
def deploy(_new, _Account):
    if _new or (currentNetwork == "development"):
        depContract = deployContracts(_Account)
    else:
        depContract = FundMe[-1]
    return depContract
        
def interAction(_new = False):
    _Account = selectAccount()
    
    depContract = deploy(_new, _Account)
    
    print(f"FundMe Contract address: {depContract.address}")
    
    print("Contract initial Balance:",depContract.getBalance())
    print("Contract Num of Donors:",depContract.numDonors())
    
    _ETH_PRICE: float = depContract.getPrice()/_ETH
    print("Current ETH price = ", _ETH_PRICE)
    
    fund(_Account, depContract, int((51/_ETH_PRICE)*_ETH + 1))
    
    print("Balance after Donation: ",depContract.getBalance())
    print("Number of Donations: ",depContract.numDonors())
    
    print("My Address total Donation:",depContract.fundAmounts(_Account)) # Calling the Value of a public variable
    
    print("\n With Drawing Funds ...")
    withDraw(_Account, depContract)
    

def main():
    print("\n\n\t*** Welcome to Brownie FundMe. ***")
    print("  *** InterActing With Deployed Contracts. ***")
    # global currentNetwork
    # currentNetwork = network.show_active()
    # ==>> ERROR : nothing in main but only Function Calls
    initialize_network()
    interAction(True)    
    
    print("\n\t*** Brownie Done. ***\n\n")
