import datetime
from typing import TypedDict


class HistoryDict(TypedDict):
    """
    User balance history dict. Used to get and set data to DB
    """
    date: str
    token_balance: float
    usdt_balance: float


class History:
    """
    Used balance history model. Used to transfer data between app modules
    """

    def __init__(
            self,
            date: datetime.datetime,
            token_balance: float,
            usdt_balance: float
    ):
        self.date = date
        self.token_balance = token_balance
        self.usdt_balance = usdt_balance

    def get_dict(self) -> HistoryDict:
        """
        Used to get data in HistoryDict format
        """
        return {
            'date': self.date.isoformat(),
            'token_balance': self.token_balance,
            'usdt_balance': self.usdt_balance
        }


class BalanceDict(TypedDict):
    """
    User balance dict. Used to get and set data to DB
    """
    wallet: str
    current_balance: float
    current_balance_usdt: float
    last_update: str
    history: list[HistoryDict]


class Balance:
    """
    User balance model. Used to transfer data between app modules
    """
    def __init__(
            self,
            wallet: str,
            current_balance: float,
            current_balance_usdt: float,
            last_update: datetime.datetime,
            history: list[History]
    ):
        self.wallet = wallet
        self.current_balance = current_balance
        self.current_balance_usdt = current_balance_usdt
        self.last_update = last_update
        self.history = history

    def get_dict(self) -> BalanceDict:
        """
        Used to get data in BalanceDict format
        """
        return {
            'wallet': self.wallet,
            'current_balance': self.current_balance,
            'current_balance_usdt': self.current_balance_usdt,
            'last_update': self.last_update.isoformat(),
            'history': [i.get_dict() for i in self.history]
        }
