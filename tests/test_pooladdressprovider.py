import pytest
from base_test import BaseTest
from aavev3 import PoolAddressProvider
from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract


class Test_PoolAddressProvider:
    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, bt):
        self.pap: PoolAddressProvider = PoolAddressProvider(bt.w3, "polygon")

    def test_init(self):
        assert isinstance(self.pap, PoolAddressProvider)
        assert isinstance(self.pap.pap, Contract)

    def test_getMarketId(self):
        result = self.pap.getMarketId()
        assert isinstance(result, str)
