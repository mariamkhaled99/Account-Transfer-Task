# Account-Transfer-Task

Small web app using Django that handles fund transfers between two accounts. The app supports importing a list of accounts with opening balances, querying these accounts, and transferring funds between any two accounts.

## Project Features

- **Account Management:** Manage accounts with details like account number, name, and balance.
- **Funds Transfer:** Transfer funds securely between accounts.
- **Transaction History:** Track and view all transaction activities.

## Examples

### Transferring Funds

Visit the [Transfer Funds](#) page to enter account details and the amount to transfer.

### Viewing Accounts

Go to the [View Accounts](#) page to see a list of all accounts and their details.

### Viewing Transaction History

Navigate to the [Transaction History](#) page to review past transactions.

## Understanding Transactions and Account Locking

Ensuring reliable and accurate transactions is crucial. Here's how transactions are managed:

### Using `transaction.atomic()`

`transaction.atomic()` makes sure that operations are performed as a single atomic transaction. If any part fails, everything is rolled back to maintain data consistency.

```python
from django.db import transaction

def transfer_funds(from_account, to_account, amount):
    with transaction.atomic():
        from_account.refresh_from_db()
        to_account.refresh_from_db()

        if from_account.balance < amount:
            raise ValueError("Insufficient funds")

        from_account.balance -= amount
        to_account.balance += amount

        from_account.save()
        to_account.save()
 ```

### Prerequisites

- Python 3.9 or later
- pip (Python package installer)
- virtualenv (optional but recommended)
- Docker (optional for containerized setup)


### Installation Steps

1. **local using venv and Django**
   ```bash
   git clone <repository-url>
   cd Account-Transfer-Task
   python -m venv venv 
   venv\Scripts\activate
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **local using Docker**
```bash
  docker-compose build
  docker-compose up
   ```
