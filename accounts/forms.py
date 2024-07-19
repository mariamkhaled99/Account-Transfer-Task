from django import forms
from .models import FileUpload,Account

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file']

class TransferForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.all())
    to_account = forms.ModelChoiceField(queryset=Account.objects.all())
    amount = forms.DecimalField(max_digits=10, decimal_places=2)


class AccountSearchForm(forms.Form):
    account_name = forms.CharField(required=False, label='Account Name')
    account_number = forms.CharField(required=False, label='Account Number')
    balance_min = forms.DecimalField(required=False, label='Min Balance', decimal_places=2, max_digits=10)
    balance_max = forms.DecimalField(required=False, label='Max Balance', decimal_places=2, max_digits=10)

