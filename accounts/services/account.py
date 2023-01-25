from audioop import add
from accounts.models.account import Account
from accounts.repositories.account import AccountRepo
from accounts.repositories.customer import CustomerRepo
from accounts.repositories.address import AddressRepo

class AccountService():
    def __init__(self, accountRepo: AccountRepo, customerRepo: CustomerRepo, addressRepo: AddressRepo) -> None:
        self.accountRepo = accountRepo
        self.customerRepo = customerRepo
        self.AddressRepo = addressRepo
    
    def open_account(self, account: Account) -> Account:
        address = self.AddressRepo.insert(account.customer_id.address)
        account.customer_id.address = address
        customer = self.customerRepo.insert(account.customer_id)
        account.customer_id = customer
        return self.accountRepo.insert(account)

    def get_all_accounts(self) -> 'list[Account]':
        accounts = self.accountRepo.get_all()
        for account in accounts:
            account.customer_id = self.customerRepo.get_by_id(account.customer_id.id)
            account.customer_id.address = self.AddressRepo.get_by_id(account.customer_id.address.id)
        return accounts

    def get_account(self, account_number: str, amount: float) -> Account:
        account = self.accountRepo.get_by_account_number(account_number)
        account.customer_id = self.customerRepo.get_by_id(account.customer_id.id)
        account.customer_id.address = self.AddressRepo.get_by_id(account.customer_id.address.id)
        return account

    def withdraw(self, account_number: str, amount: float) -> Account:
        account = self.accountRepo.get_by_account_number(account_number)
        account.balance -=amount
        self.accountRepo.update(account)
        return self.get_account(account_number)

    def deposit(self, account_number: str, amount: float) -> Account:
        account = self.accountRepo.get_by_account_number(account_number)
        account.balance +=amount
        self.accountRepo.update(account)
        return self.get_account(account_number)

    def close_account(self, account_number: str) -> None:
        account = self.get_account(account_number)
        self.accountRepo.delete(account.id)
        self.customerRepo.delete(account.customer_id.id)
        self.AddressRepo.delete(account.customer_id.address.id)