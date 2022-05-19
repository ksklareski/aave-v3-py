import pytest
from aavev3 import AaveOracle

from base_test import BaseTest
from decimal import Decimal
from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract


class Test_AaveOracle:
    @pytest.fixture(autouse=True)
    def setup_class_fixture(self, bt):
        self.oracle: AaveOracle = AaveOracle(bt.w3, "polygon")

    def test_init(self):
        assert isinstance(self.oracle, AaveOracle), "Init failed"
        assert isinstance(self.oracle.w3, Web3), "Web3 init failed"
        assert isinstance(self.oracle.oracle, Contract), "Contract init failed"

    def test_getAssetPrice(self, bt):
        price = self.oracle.getAssetPrice(bt.weth_addr)
        assert isinstance(price, Decimal), "Price type is not correct"

    def test_getAssetPrices(self, bt):
        prices = self.oracle.getAssetsPrices([bt.usdc_addr, bt.weth_addr])
        assert isinstance(prices, list), "Prices is not type list"
        for p in prices:
            assert isinstance(p, Decimal), "Price is not type Decimal"

    def test_getSourceOfAsset(self, bt):
        source = self.oracle.getSourceOfAsset(bt.weth_addr)
        assert bt.w3.isChecksumAddress(source), "Source is not type ChecksumAddress"

    def test_getFallbackOracle(self, bt):
        fallback = self.oracle.getFallbackOracle()
        assert bt.w3.isChecksumAddress(fallback), "Fallback is not type ChecksumAddress"

    def test_setAssetSources(self, bt):
        result = self.oracle.setAssetSources(
            [bt.weth_addr],
            [bt.usdc_addr],
            bt.admin_user,
        )

    def test_setFallbackOracle(self, bt):
        result = self.oracle.setFallbackOracle(bt.weth_addr, bt.admin_user)
