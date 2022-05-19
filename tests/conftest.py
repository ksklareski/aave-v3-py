import pytest
from base_test import BaseTest


@pytest.fixture(scope="session")
def bt():
    bt = BaseTest()
    bt.start_anvil()

    yield bt

    bt.stop_anvil()
