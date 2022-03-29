import json
from eth_typing import ChecksumAddress, HexStr, HexAddress
from hexbytes import HexBytes
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
        with open("../abi/IPoolAddressesProvider.json") as f:
            pap_abi: list = json.load(f)["abi"]

        # reads pool address provider contract from chain
        self.pap: Contract = w3.eth.contract(address=self.PAPADDR[network], abi=pap_abi)

    def getMarketId(self) -> str:
        return self.pap.functions.getMarketId().call()

    def getAddress(self, id: bytes) -> ChecksumAddress:
        return self.pap.functions.getAddress(id).call()

    def getPool(self) -> ChecksumAddress:
        # Gets address of pool from pool address provider
        lendingpool: ChecksumAddress = self.pap.functions.getPool().call()

        # Simple check for valid ETH address
        assert len(lendingpool) > 0 and lendingpool[0] == "0" and lendingpool[1] == "x"

        # returns pool contract
        return lendingpool

    def getPoolConfigurator(self) -> ChecksumAddress:
        return self.pap.functions.getPoolConfigurator().call()

    def getPriceOracle(self) -> ChecksumAddress:
        # Gets oracle address from pool address provider
        oracle: ChecksumAddress = self.pap.functions.getPriceOracle().call()

        # Simple check for valid ETH address
        assert len(oracle) > 0 and oracle[0] == "0" and oracle[1] == "x"

        # returns oracle contract
        return oracle

    def getACLManager(self) -> ChecksumAddress:
        return self.pap.functions.getACLManager().call()

    def getACLAdmin(self) -> ChecksumAddress:
        return self.pap.functions.getACLAdmin().call()

    def getPriceOracleSentinel(self) -> ChecksumAddress:
        return self.pap.functions.getPriceOracleSentinel().call()

    def getPoolDataProvider(self) -> ChecksumAddress:
        return self.pap.functions.getPoolDataProvider().call()

    def setMarketId(self, newMarketId: str) -> HexBytes:
        return self.pap.functions.setMarketId(newMarketId).transact()

    def setAddress(self, id: bytes, newAddress: ChecksumAddress) -> HexBytes:
        return self.pap.functions.setAddress(id, newAddress).transact()

    def setAddressAsProxy(
        self, id: bytes, newImplementationAddress: ChecksumAddress
    ) -> HexBytes:
        return self.pap.functions.setAddressAsProxy(
            id, newImplementationAddress
        ).transact()

    def setPoolImpl(self, newPoolImpl: ChecksumAddress) -> HexBytes:
        return self.pap.functions.setPoolImpl(newPoolImpl).transact()

    def setPoolConfiguratorImpl(
        self, newPoolConfiguratorImpl: ChecksumAddress
    ) -> HexBytes:
        return self.pap.functions.setPoolConfiguratorImpl(
            newPoolConfiguratorImpl
        ).transact()

    def setPriceOracle(self, newPriceOracle: ChecksumAddress) -> HexBytes:
        return self.pap.functions.setPriceOracle(newPriceOracle).transact()

    def setACLManager(self, newAclManager: ChecksumAddress) -> HexBytes:
        return self.pap.functions.setACLManager(newAclManager).transact()

    def setACLAdmin(self, newAclAdmin: ChecksumAddress) -> HexBytes:
        return self.pap.functions.setACLAdmin(newAclAdmin).transact()

    def setPriceOracleSentinel(
        self, newPriceOracleSentinel: ChecksumAddress
    ) -> HexBytes:
        return self.pap.functions.setPriceOracleSentinel(
            newPriceOracleSentinel
        ).transact()

    def setPoolDataProvider(self, newDataProvider: ChecksumAddress) -> HexBytes:
        return self.pap.functions.setPoolDataProvider(newDataProvider).transact()
