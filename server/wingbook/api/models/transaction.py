from django.db import models

from api.models.operation import Operation

class Transaction(models.Model):
    """
    Model representing a transaction.
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, default=None)

    