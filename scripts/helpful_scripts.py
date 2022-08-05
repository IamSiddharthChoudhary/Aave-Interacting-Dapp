from brownie import network, accounts, config, interface
from web3 import Web3

LOCAL_BLOCKCHAIN_NETWORKS = ["development", "ganche-cli", "mainnet-fork"]
FORKED_BLOCKCHAIN_NETWORKS = ["mainnet-fork", "mainnet-fork-dev"]


def getAccount(index=None, id=None):
    if index:
        return accounts(index)
    if network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS:
        return accounts[0]
    if id:
        return accounts.load(id)
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallet"]["from_key"])


# The address of the lending pool may change so we use the Lending pool provider address to get lending pool
# as its address remains constant
def get_Lending_Pool():
    LendingPoolAddressProvider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["LendingPoolAddressesProvider"]
    )
    LendingPoolAddress = LendingPoolAddressProvider.getLendingPool()
    """
        We'll take this address and its ABI from the interface to get the Lending pool contract.
    """
    LendingPool = interface.ILendingPool(LendingPoolAddress)
    return LendingPool


def approve_erc20(account, amount, spender, erc20Address):
    print("Approving ERC20 interface...")
    erc20 = interface.IERC20(erc20Address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    return tx


def get_borrowable_data(lendingPool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lendingPool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth of ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH.")
    return (float(available_borrow_eth), float(total_debt_eth))


def getAssetPriceInEth(priceFeed):
    priceFeedContract = interface.AggregatorV3Interface(priceFeed)
    price = priceFeedContract.latestRoundData()[1]
    convertedPrice = Web3.fromWei(price, "ether")
    print(f"The value of DAT in terms of ether is {convertedPrice}")
    return float(convertedPrice)


def repayAll(amount, account, lendingPool):
    approve_erc20(
        account,
        Web3.toWei(amount, "ether"),
        lendingPool,
        config["networks"][network.show_active()]["daiToken"],
    )
    repay_tx = lendingPool.repay(
        config["networks"][network.show_active()]["daiToken"],
        account,
        1,
        0,
        {"from": account},
    )
    repay_tx.wait(1)
    print("Repayed all")
