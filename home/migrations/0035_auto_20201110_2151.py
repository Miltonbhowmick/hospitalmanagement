# Generated by Django 2.1 on 2020-11-10 15:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_auto_20201110_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodblog',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 10, 21, 51, 23, 68974)),
        ),
    ]
