# Generated by Django 3.0 on 2020-11-25 13:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0044_auto_20201125_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodblog',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 25, 19, 12, 17, 831808)),
        ),
    ]
