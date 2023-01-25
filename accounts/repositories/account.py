from ssl import ALERT_DESCRIPTION_CERTIFICATE_UNOBTAINABLE
import psychopg2
from accounts.models.account import Account
from accounts.models.customer import Customer

class AccountRepo():
    def insert(self, account: Account) -> Account:
        with psychopg2.connect() as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO account
                        (AccountNumber, CustomerID, CurrentBalance) VALUES
                        (%(account_number)s, %(customer_id)s, %(currentBalance)s)
                        RETURNING id
                """, {
                    'account_number': account.number,
                    'customer_id': account.customer_id,
                    'currentBalance': account.balance
                })
                account.id = cursor.fetchone()[0]
        return account

    def get_by_account_number(self, account_number: str) -> Account:
        with psychopg2.connect() as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    SELECT ID, AccountNumber, CustomerID, CurrentBalance FROM
                        account WHERE AccountNumber=%(account_number)s
                """, {
                    'account_number': account_number
                })
                row = cursor.fetchone()
            return Account.construct(id=row[0], number=row[1], customer=Customer.construct(id=row[2]), balance=round(row[3], 2))

    def get_all(self) -> 'list[Account]':
        results = []
        with psychopg2.connect() as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    SELECT ID, AccountNumber, CustomerID, CurrentBalance FROM account
                """)
                rows = cursor.fetchall()
        for row in rows:
            results.append(Account.construct(id=row[0], number=row[1], customer=Customer.construct(id=row[2]), balance=round(row[3], 2)))
        return results
    
    def update(self, account: Account) -> None:
        with psychopg2.connect() as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    UPDATE account
                        SET AccountNumber=%(account_number)s, CustomerID=%(customer_id)s, CurrentBalance=%(currentBalance)s) 
                            WHERE ID=%(id)s
                """, {
                    'id': account.id,
                    'account_number': account.number,
                    'customer_id': account.customer_id,
                    'currentBalance': account.balance
                })

    def delete(self, id) -> None:
        with psychopg2.connect() as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM account WHERE ID=%(account_id)s
                """, {
                    'account_id': id
                })
