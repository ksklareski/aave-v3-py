import pytest
from base_test import BaseTest


@pytest.fixture(scope="session")
def bt():
    bt = BaseTest()
    bt.start_ganache()

    yield bt

    bt.stop_ganache()
