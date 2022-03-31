from base_test import BaseTest
from aavev3 import PoolAddressProvider

bt = None


def setup_module():
    global bt
    bt = BaseTest()
    bt.start_ganache()


def teardown_module():
    global bt
    bt.stop_ganache()


class Test_PoolAddressProvider:
    global bt

    def setup_method(self, test_method):
        self.oracle: PoolAddressProvider = PoolAddressProvider(bt.w3, "polygon")

    def test_test(self):
        pass
