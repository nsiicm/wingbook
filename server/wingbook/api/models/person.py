from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_pilot = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_main_pilot = models.BooleanField(default=False)



    class Meta:
        unique_together = ('first_name', 'last_name',)