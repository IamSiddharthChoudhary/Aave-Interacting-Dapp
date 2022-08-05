from distutils.command.config import config
from brownie import config, network, web3
from scripts.get_weth import get_weth
from scripts.helpful_scripts import (
    getAccount,
    get_Lending_Pool,
    approve_erc20,
    get_borrowable_data,
    getAssetPriceInEth,
    repayAll,
)
from web3 import Web3

amount = Web3.toWei(0.1, "ether")  # 0.1 * 10**18


def main():
    account = getAccount()
    erc20Address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()

    lendingPool = get_Lending_Pool()
    approve_erc20(account, amount, lendingPool.address, erc20Address)
    print("Depositing...")
    tx = lendingPool.deposit(
        erc20Address, amount, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited!")

    print("Getting User Data...")
    borrowableEth, totalDebt = get_borrowable_data(lendingPool, account)
    print("Recieved User Data!!")

    print("Let's Borrow DAI...")
    daiEthPrice = getAssetPriceInEth(
        config["networks"][network.show_active()]["daiEthPriceFeed"]
    )
    borrowableAmmount = (1 / daiEthPrice) * (borrowableEth * 0.80)
    # Calling the borrow function.
    daiAddress = config["networks"][network.show_active()]["daiToken"]
    borrowTx = lendingPool.borrow(
        daiAddress,
        Web3.toWei(borrowableAmmount, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrowTx.wait(1)
    print("Borrowed DAI")
    get_borrowable_data(lendingPool, account)
    repayAll(amount, account, lendingPool)
    print("Successfully performed functions in AAVE")
