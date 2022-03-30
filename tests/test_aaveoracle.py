import pytest
from aavev3 import AaveOracle
from decimal import Decimal
from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract


class Test_AaveOracle:
    def setup_method(self, test_method):
        self.w3: Web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        self.usdc_addr = self.w3.toChecksumAddress(
            "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
        )
        self.weth_addr = self.w3.toChecksumAddress(
            "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"
        )
        self.oracle: AaveOracle = AaveOracle(self.w3, "polygon")

    def test_init(self):
        assert isinstance(self.oracle, AaveOracle), "Init failed"
        assert isinstance(self.oracle.w3, Web3), "Web3 init failed"
        assert isinstance(self.oracle.oracle, Contract), "Contract init failed"

    def test_getAssetPrice(self):
        price = self.oracle.getAssetPrice(self.weth_addr)
        assert isinstance(price, Decimal), "Price type is not correct"

    def test_getAssetPrices(self):
        prices = self.oracle.getAssetsPrices([self.usdc_addr, self.weth_addr])
        assert isinstance(prices, list), "Prices is not type list"
        for p in prices:
            assert isinstance(p, Decimal), "Price is not type Decimal"

    def test_getSourceOfAsset(self):
        source = self.oracle.getSourceOfAsset(self.weth_addr)
        assert self.w3.isChecksumAddress(source), "Source is not type ChecksumAddress"

    def test_getFallbackOracle(self):
        fallback = self.oracle.getFallbackOracle()
        assert self.w3.isChecksumAddress(
            fallback
        ), "Fallback is not type ChecksumAddress"
