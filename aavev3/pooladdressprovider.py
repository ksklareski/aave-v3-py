import json
from eth_typing import ChecksumAddress, HexStr, HexAddress
from typing import Dict
from web3 import Web3
from web3.contract import Contract


class PoolAddressProvider:

    # Addresses for Pool Address Provider
    PAPADDR: Dict[str, ChecksumAddress] = {
        "arbitrum": ChecksumAddress(
            HexAddress(HexStr("0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb"))
        ),
        "avalanche": ChecksumAddress(
            HexAddress(HexStr("0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb"))
        ),
        "fantom": ChecksumAddress(
            HexAddress(HexStr("0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb"))
        ),
        "harmony": ChecksumAddress(
            HexAddress(HexStr("0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb"))
        ),
        "optimism": ChecksumAddress(
            HexAddress(HexStr("0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb"))
        ),
        "polygon": ChecksumAddress(
            HexAddress(HexStr("0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb"))
        ),
    }

    def __init__(self, w3: Web3, network: str) -> None:
        # Raise exception if the passed in network isn't supported
        if not (network in self.PAPADDR):
            raise KeyError

        # Reads pool address provider abi from file
        with open("./abi/IPoolAddressesProvider.json") as f:
            lpap_abi: list = json.load(f)["abi"]

        # reads pool address provider contract from chain
        self.lpap: Contract = w3.eth.contract(
            address=self.PAPADDR[network], abi=lpap_abi
        )

    def getPool(self) -> ChecksumAddress:
        # Gets address of pool from pool address provider
        lendingpool: ChecksumAddress = self.lpap.functions.getPool().call()

        # Simple check for valid ETH address
        assert len(lendingpool) > 0 and lendingpool[0] == "0" and lendingpool[1] == "x"

        # returns pool contract
        return lendingpool

    def getOracle(self) -> ChecksumAddress:
        # Gets oracle address from pool address provider
        oracle: ChecksumAddress = self.lpap.functions.getPriceOracle().call()

        # Simple check for valid ETH address
        assert len(oracle) > 0 and oracle[0] == "0" and oracle[1] == "x"

        # returns oracle contract
        return oracle
