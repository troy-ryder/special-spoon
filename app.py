from multiprocessing.sharedctypes import Value
import uvicorn
from fastapi import FastAPI
from accounts.models.account import Account
from accounts.services.account import AccountService
from accounts.repositories.account import AccountRepo
from accounts.repositories.customer import CustomerRepo
from accounts.repositories.address import AddressRepo
from typing import List

app = FastAPI()
addressRepo = AddressRepo()
customerRepo = CustomerRepo()
accountRepo = AccountRepo()
accountService = AccountService()

@app.post('/api/accounts')
async def open_account(account: Account) -> Account:
    if account.balance < 25.0:
        raise ValueError('$25.00 minimum required to open a new account')
    return accountService.open_account(account)

@app.get('/api/accounts', response_model=List[Account])
async def retrieve_accounts() -> List[Account]:
    return accountService.get_all_accounts()

@app.get('/api/accounts/{account_number}')
async def retrieve_account(account_number) -> Account:
    return accountService.get_account(account_number)

@app.put('/api/accounts/{account_number}/withdraw/{amount}')
async def withdraw(account_number, amount) -> Account:
    mod = float(amount)
    if mod <= 0:
        raise ValueError('Invalid withdrawal amount')
    account = accountService.get_account(account_number)
    if mod > account.balance:
        raise ValueError('Potential overdraw. Withdrawal not completed')
    return accountService.withdraw(account_number, mod)

@app.put('/api/accounts/{account_number}/deposit/{amount}')
async def withdraw(account_number, amount) -> Account:
    mod = float(amount)
    if mod <= 0:
        raise ValueError('Invalid deposit amount')
    return accountService.deposit(account_number, mod)

@app.delete('/api/accounts/{account_number}')
async def close_account(account_number) -> None:
    accountService.close_account(account_number)
    
if __name__ == "__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=8080,reload=True) #,timeout_keep_alive=3600,debug=True,workers=10)