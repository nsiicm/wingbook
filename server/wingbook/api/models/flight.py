from django.db import models


class Flight(models.Model):
    date = models.DateField()
    departure_airport = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_airport = models.CharField(max_length=100)
    arrival_time = models.TimeField()
    plane = models.ForeignKey('Plane', on_delete=models.PROTECT)
    se_duration = models.DurationField(default="00:00:00")
    me_duration = models.DurationField(default="00:00:00")
    multi_pilot_duration = models.DurationField(default="00:00:00")
    flight_duration = models.DurationField()
    pilot_in_command = models.ForeignKey('Person', related_name='pilot_in_command', on_delete=models.PROTECT)
    landing_day_num = models.IntegerField(default=0)
    landing_night_num = models.IntegerField(default=0)
    ifr_apch_num = models.IntegerField(default=0)
    night_duration = models.DurationField(default="00:00:00")
    ifr_duration = models.DurationField(default="00:00:00")
    pilot_in_command_duration = models.DurationField(default="00:00:00")
    copilot_duration = models.DurationField(default="00:00:00")
    dual_duration = models.DurationField(default="00:00:00")
    instructor_duration = models.DurationField(default="00:00:00")
    simulator_date = models.DateField(blank=True, null=True)
    simulator_type = models.CharField(max_length=100, blank=True, null=True)
    simulator_duration = models.DurationField(blank=True, null=True)
    comments = models.TextField(blank=True)
    passengers = models.ManyToManyField('Person', related_name='passengers', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    passengers_perc = models.JSONField(blank=True, null=True)
    #{
    # ID : PERC,
    #}
    #
    #
    #