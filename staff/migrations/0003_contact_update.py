# Generated by Django 3.0 on 2020-12-22 05:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_auto_20201222_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='update',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
