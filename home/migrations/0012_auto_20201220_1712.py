# Generated by Django 3.0 on 2020-12-20 11:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20201214_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodblog',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='foodblogview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 20, 17, 12, 39, 319821)),
        ),
    ]
