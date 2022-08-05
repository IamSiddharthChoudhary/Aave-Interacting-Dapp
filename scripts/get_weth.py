from scripts.helpful_scripts import getAccount
from brownie import config, network, interface


def get_weth():
    """Mints WETH by depositing ETH"""
    # For interacting with the contracts we need two things:s
    # ABI
    # Address
    account = getAccount()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1 * 10**18})
    tx.wait(1)
    print("Recieved 0.1 WETH")
    return tx


def main():
    get_weth()
