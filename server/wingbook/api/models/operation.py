from django.db import models


class Operation(models.Model):
    """
    Operation model representing an operation in the system.
    """
    type = models.CharField(max_length=100, choices=[
        ('debit','Debit'),
        ('credit','Credit'),
        ('refund','Refund'),
        ('transfer','Transfer'),
    ])
    date = models.DateField()
    source_account = models.ForeignKey('Account', on_delete=models.PROTECT, related_name='source_account', blank=True, null=True)
    destination_account = models.ForeignKey('Account', on_delete=models.PROTECT, related_name='destination_account')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE, blank=True, null=True)


    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        print(is_new)
        if is_new:
            from api.models.transaction import Transaction  # Avoid circular import if needed
            print(f"Creating transaction for operation : {self.type}")
            if self.type == 'credit':
                print("Creating credit transaction")
                Transaction.objects.create(
                    account=self.destination_account,
                    amount=self.amount,
                    operation=self
                )
            elif self.type == 'debit':
                print("Creating debit transaction")
                Transaction.objects.create(
                    account=self.destination_account,
                    amount=-self.amount,
                    operation=self
                )
            elif self.type == 'transfer':
                print("Creating transfer transaction")
                Transaction.objects.create(
                    account=self.source_account,
                    amount=-self.amount,
                    operation=self
                )
                Transaction.objects.create(
                    account=self.destination_account,
                    amount=self.amount,
                    operation=self
                )
            elif self.type == 'refund':
                print("Creating refund transaction")
                Transaction.objects.create(
                    account=self.source_account,
                    amount=self.amount,
                    operation=self
                )
                Transaction.objects.create(
                    account=self.destination_account,
                    amount=self.amount,
                    operation=self
                )
