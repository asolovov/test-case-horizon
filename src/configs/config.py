import os
from .errors import *


class Config:
    """
    Used to store app configurations
    """
    def __init__(
            self,
            db: str,
            db_name: str,
            table_balance: str,
            web3_provider: str,
            contract_address: str,
            token_id: str,
            debug: bool
    ):
        self.DB = db
        self.db_name = db_name
        self.table_balance = table_balance
        self.web3_provider = web3_provider
        self.contract_address = contract_address
        self.token_id = token_id
        self.debug = debug


def get_config() -> Config:
    """
    Used to set app configurations from .env file or set default values
    :return: config instance
    """
    db = os.getenv('DB')
    if db is None:
        raise NoDbConnectString

    db_name = os.environ.get('DB_NAME', 'test_case_1_solovov_db')
    table_balance = os.environ.get('TABLE_BALANCE', 'table_balances')
    web3_provider = os.environ.get('WEB3_PROVIDER', 'https://rpc.eth.gateway.fm')
    contract_address = os.environ.get('CONTRACT_ADDRESS', '0xD533a949740bb3306d119CC777fa900bA034cd52')
    token_id = os.environ.get('TOKEN_ID', 'curve-dao-token')
    debug = os.getenv('DEBUG') == 'true'

    return Config(db, db_name, table_balance, web3_provider, contract_address, token_id, debug)

