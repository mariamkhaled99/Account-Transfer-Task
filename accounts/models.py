from django.db import models
from django.core.exceptions import ValidationError
import os
from django.db import models
from django.utils import timezone

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.csv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class Account(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    account_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.account_name} ({self.account_number})"

class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/', validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    


class TransactionHistory(models.Model):
    from_account = models.ForeignKey('Account', related_name='transactions_from', on_delete=models.CASCADE)
    to_account = models.ForeignKey('Account', related_name='transactions_to', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.amount} from {self.from_account} to {self.to_account} on {self.timestamp}"

