from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=100)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, blank=True, null=True)
    
    def get_balance(self):
        """
        Calculate the balance of the account.
        """
        transactions = self.transaction_set.filter(account=self)
        balance = sum(transaction.amount for transaction in transactions)
        return balance