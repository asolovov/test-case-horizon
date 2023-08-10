from fastapi import FastAPI, HTTPException
from web3 import Web3

from repository.repository import get_repository
from service.service import get_balance_service
from configs.config import get_config
from contract.contract import get_contract

conf = get_config()
rep = get_repository(conf)
contract = get_contract(conf)
srv = get_balance_service(rep, contract)

app = FastAPI(title="Test Case 1 for Horizon DEX")


@app.get('/balance/current/{addr}')
def get_current_balance(addr: str):
    if Web3.is_address(addr):
        return srv.get_and_set_balances(addr)
    else:
        raise HTTPException(status_code=400, detail='bad address')


@app.get('/balance/history/{addr}')
def get_user_history(addr: str):
    if Web3.is_address(addr):
        return srv.get_history(addr)
    else:
        raise HTTPException(status_code=400, detail='bad address')