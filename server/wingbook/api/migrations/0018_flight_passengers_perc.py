# Generated by Django 5.2.1 on 2025-05-20 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_remove_flight_operations_operation_flight'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='passengers_perc',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
