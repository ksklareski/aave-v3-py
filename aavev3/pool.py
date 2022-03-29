import json
from . import abi
from decimal import Decimal
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from .pooladdressprovider import PoolAddressProvider
from typing import List, Union
from web3 import Web3
from web3.contract import Contract

# NOTE: Shamelessly stolen from https://stackoverflow.com/a/20885799
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources


class Pool:
    def __init__(self, w3: Web3, network: str) -> None:
        self.w3 = w3

        pap: PoolAddressProvider = PoolAddressProvider(self.w3, network)
        pool_address: ChecksumAddress = pap.getPool()

        # Reads lending pool abi from file
        # with open("./abi/IPool.json") as f:
        with pkg_resources.open_text(abi, "IPool.json") as f:
            self.pool_abi: list = json.load(f)["abi"]
        self.pool: Contract = w3.eth.contract(address=pool_address, abi=self.pool_abi)

    # NOTE: Write Methods
    def mintUnbacked(
        self,
        asset: ChecksumAddress,
        amount: Decimal,
        onBehalfOf: ChecksumAddress,
        referralCode: Decimal = Decimal("0"),
    ) -> HexBytes:
        # TODO: Make onBehalfOf msg.sender unless specified
        return self.pool.functions.mintUnbacked(
            asset, amount, onBehalfOf, referralCode
        ).transact()

    def backUnbacked(
        self, asset: ChecksumAddress, amount: Decimal, fee: Decimal
    ) -> HexBytes:
        return self.pool.functions.backUnbacked(asset, amount, fee).transact()

    def rescueTokens(
        self, token: ChecksumAddress, to: ChecksumAddress, amount: Decimal
    ) -> HexBytes:
        return self.pool.functions.rescueTokens(token, to, amount).transact()

    def supply(
        self,
        asset: ChecksumAddress,
        amount: Decimal,
        onBehalfOf: ChecksumAddress,
        referralCode: Decimal = Decimal("0"),
    ) -> HexBytes:
        return self.pool.functions.supply(
            asset, amount, onBehalfOf, referralCode
        ).transact()

    def supplyWithPermit(
        self,
        asset: ChecksumAddress,
        amount: Decimal,
        onBehalfOf: ChecksumAddress,
        deadline: Decimal,
        permitV: Decimal,
        permitR: bytes,
        permitS: bytes,
        referralCode: Decimal = Decimal("0"),
    ) -> HexBytes:
        return self.pool.functions.supplyWithPermit(
            asset, amount, onBehalfOf, referralCode, deadline, permitV, permitR, permitS
        ).transact()

    def withdraw(
        self, asset: ChecksumAddress, amount: Decimal, to: ChecksumAddress
    ) -> HexBytes:
        return self.pool.functions.withdraw(asset, amount, to).transact()

    def borrow(
        self,
        asset: ChecksumAddress,
        amount: Decimal,
        interestRateMode: Decimal,
        onBehalfOf: ChecksumAddress,
        referralCode: Decimal = Decimal("0"),
    ) -> HexBytes:
        return self.pool.functions.borrow(
            asset, amount, interestRateMode, referralCode, onBehalfOf
        ).transact()

    def repay(
        self,
        asset: ChecksumAddress,
        amount: Decimal,
        rateMode: Decimal,
        onBehalfOf: ChecksumAddress,
    ) -> HexBytes:
        return self.pool.functions.repay(asset, amount, rateMode, onBehalfOf).transact()

    def repayWithPermit(
        self,
        asset: ChecksumAddress,
        amount: Decimal,
        interestRateMode: Decimal,
        onBehalfOf: ChecksumAddress,
        deadline: Decimal,
        permitV: Decimal,
        permitR: bytes,
        permitS: bytes,
    ) -> HexBytes:
        return self.pool.functions.repayWithPermit(
            asset,
            amount,
            interestRateMode,
            onBehalfOf,
            deadline,
            permitV,
            permitR,
            permitS,
        ).transact()

    def repayWithATokens(
        self, asset: ChecksumAddress, amount: Decimal, interestRateMode: Decimal
    ) -> HexBytes:
        return self.pool.functions.repayWithATokens(
            asset, amount, interestRateMode
        ).transact()

    def swapBorrowRateMode(self, asset: ChecksumAddress, rateMode: Decimal) -> HexBytes:
        return self.pool.functions.swapBorrowRateMode(asset, rateMode).transact()

    def rebalanceStableBorrowRate(
        self, asset: ChecksumAddress, user: ChecksumAddress
    ) -> HexBytes:
        return self.pool.functions.rebalanceStableBorrowRate(asset, user).transact()

    def setUserUseReserveAsCollateral(
        self, asset: ChecksumAddress, useAsCollateral: bool
    ) -> HexBytes:
        return self.pool.functions.setUserUseReserveAsCollateral(
            asset, useAsCollateral
        ).transact()

    def liquidationCall(
        self,
        collateral: ChecksumAddress,
        debt: ChecksumAddress,
        user: ChecksumAddress,
        debtToCover: Decimal,
        receiveAToken: bool,
    ) -> HexBytes:
        return self.pool.functions.liquidationCall(
            collateral, debt, user, debtToCover, receiveAToken
        ).transact()

    def flashLoan(
        self,
        receiverAddress: ChecksumAddress,
        assets: List[ChecksumAddress],
        amounts: List[Decimal],
        interestRateModes: List[Decimal],
        onBehalfOf: ChecksumAddress,
        params: bytes,
        referralCode: Decimal = Decimal("0"),
    ) -> HexBytes:
        return self.pool.functions.flashLoan(
            receiverAddress,
            assets,
            amounts,
            interestRateModes,
            onBehalfOf,
            params,
            referralCode,
        ).transact()

    def flashLoanSimple(
        self,
        receiverAddress: ChecksumAddress,
        asset: ChecksumAddress,
        amount: Decimal,
        params: bytes,
        referralCode: Decimal = Decimal("0"),
    ) -> HexBytes:
        return self.pool.functions.flashLoanSimple(
            receiverAddress, asset, amount, params, referralCode
        ).transact()

    def mintToTreasury(self, assets: List[ChecksumAddress]) -> HexBytes:
        return self.pool.functions.mintToTreasury(assets).transact()

    def setUserEMode(self, categoryId: Decimal) -> HexBytes:
        return self.pool.functions.setUserEMode(categoryId).transact()

    # NOTE: Read Methods
    def getReserveData(
        self, asset: ChecksumAddress
    ) -> List[Union[Decimal, ChecksumAddress]]:
        return self.pool.functions.getReserveData(asset).call()

    def getUserAccountData(self, user: ChecksumAddress) -> List[Decimal]:
        return self.pool.functions.getUserAccountData(user).call()

    def getConfiguration(self, asset: ChecksumAddress) -> Decimal:
        return self.pool.functions.getConfiguration(asset).call()

    def getUserConfiguration(self, user: ChecksumAddress) -> Decimal:
        return self.pool.functions.getUserConfiguration(user).call()

    def getReserveNormalizedIncome(self, asset: ChecksumAddress) -> Decimal:
        return self.pool.functions.getReserveNormalizedIncome(asset).call()

    def getReserveNormalizedDebt(self, asset: ChecksumAddress) -> Decimal:
        return self.pool.functions.getReserveNormalizedVariableDebt(asset).call()

    def getReservesList(self) -> List[ChecksumAddress]:
        return self.pool.functions.getReservesList().call()

    def getEModeCategoryData(
        self, id: Decimal
    ) -> List[Union[Decimal, Decimal, Decimal, ChecksumAddress, str]]:
        return self.pool.functions.getEModeCategoryData(id).call()

    def getUserEMode(self, user: ChecksumAddress) -> Decimal:
        return self.pool.functions.getUserEMode(user).call()

    def FLASHLOAN_PREMIUM_TOTAL(self) -> Decimal:
        return self.pool.functions.FLASHLOAN_PREMIUM_TOTAL().call()

    def FLASHLOAN_PREMIUM_TO_PROTOCOL(self) -> Decimal:
        return self.pool.functions.FLASHLOAN_PREMIUM_TO_PROTOCOL().call()
