# Generated by Django 3.0 on 2020-12-09 09:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0052_auto_20201206_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodblog',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 9, 15, 53, 49, 539761)),
        ),
    ]
