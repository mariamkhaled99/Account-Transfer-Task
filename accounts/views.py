
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account
from .forms import FileUploadForm, TransferForm,AccountSearchForm
import json,os
from django.conf import settings
import pandas as pd
from django.core.paginator import Paginator
from django.db import transaction
from django.db import transaction, IntegrityError
from .models import TransactionHistory




def transaction_history(request):
    # Retrieve all transactions, ordered by timestamp in descending order
    transactions = TransactionHistory.objects.all().order_by('-timestamp')
    return render(request, 'accounts/transaction_history.html', {'transactions': transactions})

def handle_uploaded_file(file):
    # Use the file's name to determine its location
    file_name = file.name
    
    # Construct the file path using media root
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)
    
    # Check if file exists at the given path
    if os.path.exists(file_path):
           
            accounts_json = csv_to_json(file_path)
            
            accounts_data = json.loads(accounts_json)
            print("Accounts Data:", accounts_data)  # Debug print

            # Save data to the database
            for account_data in accounts_data:
                account_number = account_data.get('ID')
                account_name = account_data.get('Name')
                balance = float(account_data.get('Balance', 0))  # Ensure balance is converted to float

                Account.objects.update_or_create(
                    account_number=account_number,
                    defaults={'account_name': account_name, 'balance': balance}
                )
    else:
        print(f"File does not exist at: {file_path}")


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("Uploaded File:", request.FILES['file'])
            handle_uploaded_file(request.FILES['file'])
            messages.success(request, 'File uploaded and accounts imported successfully!')
            return redirect('list_accounts')
    else:
        form = FileUploadForm()
    return render(request, 'accounts/upload_file.html', {'form': form})





def csv_to_json(file):
    print("file:{file}")
    df = pd.read_csv(file)

    # Convert DataFrame to JSON
    json_data = df.to_json(orient='records')

    # Convert to JSON
    return json_data




def list_accounts(request):
    form = AccountSearchForm(request.GET or None)
    accounts_list = Account.objects.all()

    if form.is_valid():
        account_name = form.cleaned_data.get('account_name')
        account_number = form.cleaned_data.get('account_number')
        balance_min = form.cleaned_data.get('balance_min')
        balance_max = form.cleaned_data.get('balance_max')

        if account_name:
            accounts_list = accounts_list.filter(account_name__icontains=account_name)
        if account_number:
            accounts_list = accounts_list.filter(account_number=account_number)
        if balance_min is not None:
            accounts_list = accounts_list.filter(balance__gte=balance_min)
        if balance_max is not None:
            accounts_list = accounts_list.filter(balance__lte=balance_max)

    paginator = Paginator(accounts_list, 10)  # Show 10 accounts per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/list_accounts.html', {'form': form, 'page_obj': page_obj})

def home(request):
    return render(request, 'accounts/home.html')



def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']
            if from_account.balance == 0:
                    messages.error(request, 'Source account has zero balance. Transfer not allowed.')
                    return redirect('transfer_funds')
            
            if from_account.balance < amount:
                messages.error(request, 'Insufficient balance in the source account.')
                return redirect('transfer_funds')
            
            try:
                with transaction.atomic():
                    # Lock the rows for the duration of the transaction
                    from_account = Account.objects.select_for_update().get(pk=from_account.pk)
                    to_account = Account.objects.select_for_update().get(pk=to_account.pk)

                    if from_account.balance >= amount:
                        from_account.balance -= amount
                        to_account.balance += amount
                        from_account.save()
                        to_account.save()
                        
                        # Create a transaction history record
                        TransactionHistory.objects.create(
                            from_account=from_account,
                            to_account=to_account,
                            amount=amount
                        )
                        
                        messages.success(request, f'Funds transferred successfully from {from_account} to {to_account}!')
                    else:
                        messages.error(request, 'Insufficient balance in the source account.')
            except IntegrityError:
                messages.error(request, 'Transaction failed due to a concurrent update.')
            return redirect('transaction_history')
    else:
        form = TransferForm()
    return render(request, 'accounts/transfer_funds.html', {'form': form})


