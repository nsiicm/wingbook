from django.db import models

class Plane(models.Model):
    model = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20, unique=True)
    single_engine = models.BooleanField(default=True)
    single_pilot = models.BooleanField(default=True)
    hour_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    instructor_hour_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    account = models.ForeignKey('Account', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.registration_number