# Generated by Django 3.0 on 2020-12-12 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sell', '0004_auto_20201212_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
