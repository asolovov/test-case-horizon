from datetime import datetime
import json
import urllib.request, urllib.error
from abc import ABC, abstractmethod

from fastapi import HTTPException
from web3 import Web3

from repository.repository import IRepository
from contract.contract import IContract
from model.balance_models import Balance, History


class IService(ABC):
    """
    Service interface. Used to operate Contact and Repository layers
    """
    repository: IRepository

    @abstractmethod
    def get_and_set_balances(self, addr: str) -> dict:
        """
        Used to get user balance from contract and set data to DB

        :param addr: user waller
        :return json-like dict
        """
        raise NotImplementedError

    @abstractmethod
    def get_history(self, addr: str) -> dict:
        """
        Used to get user balance history from DB

        :param addr: user wallet
        :return: json-like dict
        """
        raise NotImplementedError


class BalanceService(IService):
    """
    Implementation of service interface
    """
    def __init__(self, repository: IRepository, contract: IContract):
        self.repository = repository
        self.contract = contract

    def get_and_set_balances(self, addr: str) -> dict:
        balance = self.contract.balance_of(addr)
        balance = float(round(Web3.from_wei(balance, 'ether'), 4))

        try:
            response: bytes = urllib.request.urlopen(
                'https://api.coingecko.com/api/v3/simple/price?ids=curve-dao-token&vs_currencies=usd'
            ).read()
        except urllib.error.URLError as e:
            raise HTTPException(status_code=500, detail=f'coingeco error: {e.reason}')

        response: dict = json.loads(response.decode('utf-8'))
        usdt_token_price = float(response['curve-dao-token']['usd'])

        usd_balance = round(balance * usdt_token_price, 4)

        self.repository.add_user_balance(Balance(
            wallet=addr,
            current_balance=balance,
            current_balance_usdt=usd_balance,
            last_update=datetime.now(),
            history=[History(
                date=datetime.now(),
                token_balance=balance,
                usdt_balance=usd_balance
            )]
        ))

        return {'balance_token': balance, 'balance_usdt': usd_balance}

    def get_history(self, addr: str):
        history = self.repository.get_user_balance(addr)
        if history is None:
            raise HTTPException(status_code=404, detail='address not found')
        else:
            return {'history': history}


def get_balance_service(rep: IRepository, contract: IContract) -> IService:
    """
    Used to get service instance that implements IService interface

    :param rep: repository instance
    :param contract: contract instance
    :return: service instance
    """
    return BalanceService(rep, contract)
