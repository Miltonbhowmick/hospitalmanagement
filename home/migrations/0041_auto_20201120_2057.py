# Generated by Django 2.1 on 2020-11-20 14:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0040_auto_20201120_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodblog',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 20, 20, 57, 7, 233176)),
        ),
    ]
