import pytest
from base_test import BaseTest
from aavev3 import PoolAddressProvider
from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract


class Test_PoolAddressProvider:
    @pytest.fixture(autouse=True)
    def setup_class_fixture(self, bt):
        self.pap: PoolAddressProvider = PoolAddressProvider(bt.w3, "polygon")

    def test_init(self):
        assert isinstance(self.pap, PoolAddressProvider)
        assert isinstance(self.pap.pap, Contract)

    def test_getMarketId(self):
        result = self.pap.getMarketId()
        assert isinstance(result, str)

    def test_getAddress(self, bt):
        result = self.pap.getAddress(
            "0x19c860a63258efbd0ecb7d55c626237bf5c2044c26c073390b74f0c13c857433"
        )
        assert bt.w3.isChecksumAddress(result)

    def test_getPool(self, bt):
        result = self.pap.getPool()
        assert bt.w3.isChecksumAddress(result)
