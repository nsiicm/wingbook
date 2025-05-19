from django.db import models

class Plane(models.Model):
    model = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20, unique=True)
    single_engine = models.BooleanField(default=True)
    single_pilot = models.BooleanField(default=True)

    def __str__(self):
        return self.registration_number