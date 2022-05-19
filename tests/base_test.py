import anvil
from web3 import Web3


class BaseTest:
    w3 = None
    usdc_addr = None
    weth_addr = None
    admin_user = None

    def start_anvil(self):
        anvil.start_anvil()

        self.w3: Web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

        self.usdc_addr = self.w3.toChecksumAddress(
            "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
        )
        self.weth_addr = self.w3.toChecksumAddress(
            "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"
        )
        self.admin_user = anvil.admin_user

    def stop_anvil(self):
        anvil.stop_anvil()

        self.w3 = None
