import datetime
from abc import ABC, abstractmethod

from pymongo import MongoClient
from pymongo.server_api import ServerApi

from configs.config import Config
from model.balance_models import Balance, BalanceDict, HistoryDict
from .errors import PingDBError


class IRepository(ABC):
    """
    Repository interface. Used to operate DB
    """

    @abstractmethod
    def add_user_balance(self, balance: Balance) -> None:
        """
        Used to add given user balance to DB

        :param balance: user balance object from model module
        :return: None
        """
        raise NotImplementedError

    # get_user_balance is used to get user balance by given user address
    @abstractmethod
    def get_user_balance(self, address: str) -> HistoryDict:
        """
        Used to get user balance history from DB

        :param address: user wallet address
        :return: user history from DB as HistoryDict
        """
        raise NotImplementedError


# Repository is an implementation of IRepository using Mango DB
class Repository(IRepository):
    def __init__(self, conf: Config):
        client = MongoClient(conf.DB, server_api=ServerApi('1'))
        ping: dict = client.admin.command('ping')

        if ping['ok'] != 1:
            raise PingDBError

        db = client[conf.db_name]
        table_balance = db[conf.table_balance]

        self.table_balance = table_balance

    def add_user_balance(self, balance: Balance):
        db_balance: BalanceDict = self.table_balance.find_one({'wallet': balance.wallet})

        if db_balance is None:
            self.table_balance.insert_one(balance.get_dict())
        else:
            history: list[HistoryDict] = db_balance['history']
            history.append(balance.history[0].get_dict())
            self.table_balance.update_one(
                {'wallet': balance.wallet},
                {'$set': {'last_update': datetime.datetime.now(), 'history': history}}
            )

    def get_user_balance(self, address: str) -> HistoryDict:
        db_balance: BalanceDict = self.table_balance.find_one({'wallet': address})

        if db_balance is None:
            return None
        else:
            return db_balance['history']


def get_repository(conf: Config) -> IRepository:
    """
    Used to get repository instance

    :param conf: app configurations
    :return: repository instance that implements IRepository interface
    """
    return Repository(conf)

