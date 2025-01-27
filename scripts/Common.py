from brownie import accounts, config, network

_ETH    = 1000000000000000000
_Gwei   = 1000000000
_Wei    = 1

class myAccount:
    def __init__(self, currentNetwork):
        self.network = currentNetwork # type: ignore
        
    def useDevAccounts(self):
        return accounts[0]
        
    def useFujiSecureAccounts(self): 
        # It NEEDS: RPC Declaration
        return accounts.load("dev-FujiAvalanche")
    
    def useSepoliaSecureAccounts(self): 
        # It Needs: $WEB3_INFURA_PROJECT_ID
        return accounts.load("dev-Sepolia")
    
    def useForkSecureAccounts(self): 
        # It Needs: $WEB3_INFURA_PROJECT_ID
        return accounts.load("dev-MainChain")

    def useEnvironmentAccounts(self):
        return accounts.add(config["wallets"]["ganacheUI_key"]) # accounts[0] also Works for GanacheUI
        # return accounts[0]
    
    def autoAccount(self):
        
        if self.network == "avax-test":
            return self.useFujiSecureAccounts()
        elif self.network == "sepolia":
            return self.useSepoliaSecureAccounts()
        elif self.network == "ganacheUI":
            return self.useEnvironmentAccounts()
        elif self.network == "development":
            return self.useDevAccounts()
        elif "mainnet-fork" in self.network:
            return self.useDevAccounts()
        else:
            return None