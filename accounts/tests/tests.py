import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import Account, TransactionHistory
from accounts.forms import FileUploadForm, TransferForm, AccountSearchForm
from django.db import IntegrityError



@pytest.fixture
def account():
    return Account.objects.create(
        account_number='123456',
        account_name='Test Account',
        balance=1000.00
    )

@pytest.fixture
def transaction_history():
    return TransactionHistory.objects.create(
        from_account=1,
        to_account=2,
        amount=100.00
    )

@pytest.mark.django_db
def test_home_view(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Welcome to the Account Management System' in response.content.decode()

@pytest.mark.django_db
def test_list_accounts_view(client, account):
    url = reverse('list_accounts')
    response = client.get(url)
    assert response.status_code == 200
    assert account.account_number in response.content.decode()

@pytest.mark.django_db
def test_transaction_history_view(client):
    url = reverse('transaction_history')
    response = client.get(url)
    assert response.status_code == 200
    

@pytest.mark.django_db
def test_upload_file_view(client):
   
    file_content = b"ID,Name,Balance\n123,Test User,500.00"
    file = SimpleUploadedFile("test_file.csv", file_content, content_type="text/csv")
    url = reverse('upload_file')
    response = client.post(url, {'file': file})
    assert response.status_code == 302 
    assert Account.objects.filter(account_number='123').exists()

@pytest.mark.django_db
def test_transfer_funds_view(client, account):
    
    url = reverse('transfer_funds')
    # Create another account to transfer funds to
    to_account = Account.objects.create(
        account_number='654321',
        account_name='Another Account',
        balance=500.00
    )
    response = client.post(url, {
        'from_account': account.pk,
        'to_account': to_account.pk,
        'amount': 100.00
    })
    assert response.status_code == 302  # Redirect after successful transfer
    account.refresh_from_db()
    to_account.refresh_from_db()
    assert account.balance == 900.00
    assert to_account.balance == 600.00
    assert TransactionHistory.objects.exists()

@pytest.mark.django_db
def test_search_accounts_view(client, account):
    url = reverse('list_accounts') + '?account_name=Test Account'
    response = client.get(url)
    assert response.status_code == 200
    assert account.account_name in response.content.decode()
