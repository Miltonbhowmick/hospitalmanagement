# Generated by Django 2.0 on 2020-07-11 04:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_foodblog_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='urgent_resolve',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='foodblog',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 7, 11, 10, 34, 54, 340109)),
        ),
    ]