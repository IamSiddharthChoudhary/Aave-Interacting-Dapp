from brownie import network, config, interface
from scripts.helpful_scripts import approve_erc20, get_Lending_Pool, getAccount
from scripts.get_weth import get_weth

amount = 1 * 10**18


def test_get_weth():
    account = getAccount()
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    erc20Address = config["networks"][network.show_active()]["weth_token"]
    wethContract = interface.IERC20(erc20Address)
    balance = wethContract.balanceOf(account)
    assert balance > 0


def test_approve():
    account = getAccount()
    lendingPool = get_Lending_Pool()
    erc20Addresses = config["networks"][network.show_active()]["weth_token"]
    tx = approve_erc20(account, amount, lendingPool, erc20Addresses)
    assert tx is not True
