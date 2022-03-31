import pytest
import os
import signal
import socket
import subprocess
import time

from aavev3 import AaveOracle
from decimal import Decimal
from dotenv import load_dotenv
from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract

p = None


def setup_module():
    global p
    load_dotenv(override=True)
    poly_url = os.environ["POLY_URL"]

    # Start ganache cli
    p = subprocess.Popen(
        [
            "ganache",
            "-f",
            poly_url,
            "-i",
            "999",
            "-e",
            "1000000",
            "-p",
            "8545",
            "-l",
            "8000000",
            "-u",
            "0x4365F8e70CF38C6cA67DE41448508F2da8825500",
        ]
    )
    wait_for_port(port="8545", timeout=10)


def wait_for_port(port, host="localhost", timeout=5.0):
    """Wait until a port starts accepting TCP connections.
    Args:
        port (int): Port number.
        host (str): Host address on which the port should exist.
        timeout (float): In seconds. How long to wait before raising errors.
    Raises:
        TimeoutError: The port isn't accepting connection after time specified in `timeout`.
    """
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as ex:
            time.sleep(0.01)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError(
                    "Waited too long for the port {} on host {} to start accepting "
                    "connections.".format(port, host)
                ) from ex


def teardown_module():
    global p
    os.kill(p.pid, signal.SIGTERM)


class Test_AaveOracle:

    admin_user = Web3.toChecksumAddress("0x4365F8e70CF38C6cA67DE41448508F2da8825500")

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

    def test_setAssetSources(self):
        result = self.oracle.setAssetSources(
            [self.weth_addr],
            [self.usdc_addr],
            self.admin_user,
        )

    def test_setFallbackOracle(self):
        result = self.oracle.setFallbackOracle(self.weth_addr, self.admin_user)
