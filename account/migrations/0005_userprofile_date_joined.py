# Generated by Django 3.0 on 2020-12-20 16:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_userprofile_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
