# Generated by Django 5.2.1 on 2025-05-20 09:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_remove_account_is_main_account_plane_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='transaction_type',
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('flight', 'Flight'), ('credit', 'Credit'), ('refund', 'Refund')], max_length=100)),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('destination_account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destination_account', to='api.account')),
                ('source_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='source_account', to='api.account')),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='operation',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.operation'),
        ),
    ]
