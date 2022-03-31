import json
from . import abi
from decimal import Decimal
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from .pooladdressprovider import PoolAddressProvider
from typing import List
from web3 import Web3

# NOTE: Shamelessly stolen from https://stackoverflow.com/a/20885799
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources


class AaveOracle:
    def __init__(self, w3: Web3, network: str):
        self.w3 = w3

        pap: PoolAddressProvider = PoolAddressProvider(self.w3, network)
        oracle_address: ChecksumAddress = pap.getPriceOracle()

        # Reads oracle abi from file
        with pkg_resources.open_text(abi, "IAaveOracle.json") as f:
            self.oracle_abi: list = json.load(f)["abi"]
        self.oracle = w3.eth.contract(address=oracle_address, abi=self.oracle_abi)

    def getAssetPrice(self, asset: ChecksumAddress) -> Decimal:
        return Decimal(self.oracle.functions.getAssetPrice(asset).call())

    def getAssetsPrices(self, assets: List[ChecksumAddress]) -> List[Decimal]:
        prices = self.oracle.functions.getAssetsPrices(assets).call()
        return [Decimal(p) for p in prices]

    def getSourceOfAsset(self, asset: ChecksumAddress) -> ChecksumAddress:
        return self.w3.toChecksumAddress(
            self.oracle.functions.getSourceOfAsset(asset).call()
        )

    def getFallbackOracle(self) -> ChecksumAddress:
        return self.w3.toChecksumAddress(
            self.oracle.functions.getFallbackOracle().call()
        )

    def setAssetSources(
        self,
        assets: List[ChecksumAddress],
        sources: List[ChecksumAddress],
        from_account: ChecksumAddress,
    ) -> HexBytes:
        return self.oracle.functions.setAssetSources(assets, sources).transact(
            {"from": from_account}
        )

    def setFallbackOracle(
        self, fallbackOracle: ChecksumAddress, from_account: ChecksumAddress
    ) -> HexBytes:
        return self.oracle.functions.setFallbackOracle(fallbackOracle).transact(
            {"from": from_account}
        )
