from abc import ABC, abstractmethod

from web3 import Web3

from configs.config import Config
from .errors import ProviderNotConnected, BadContractAddress


class IContract(ABC):
    """
    Contract interface, used to operate deployed smart-contract on ETH chain
    """
    @abstractmethod
    def balance_of(self, address: str) -> str:
        """
        Balance of contract function

        :param address: wallet address
        :return: wallet token balance
        """
        raise NotImplementedError


class Contract(IContract):
    """
    Implementation of IContract interface. Web3 lib is used
    """
    def __init__(self, config: Config):
        provider = Web3(Web3.HTTPProvider(config.web3_provider))
        is_connected = provider.is_connected()

        if not is_connected:
            raise ProviderNotConnected

        is_address = Web3.is_checksum_address(config.contract_address)

        if not is_address:
            raise BadContractAddress

        addr = Web3.to_checksum_address(config.contract_address)
        abi = open('./src/contract/abi.json').read()
        contract = provider.eth.contract(address=addr, abi=abi)

        self.contract = contract

    def balance_of(self, address: str) -> int:
        addr = Web3.to_checksum_address(address)
        balance = self.contract.functions.balanceOf(addr).call()
        return balance


def get_contract(config: Config) -> IContract:
    """
    Used to get contract instance that implements IContract interface

    :param config: app configurations
    :return: contract instance
    """
    return Contract(config)

