# Generated by Django 2.0 on 2020-07-10 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200708_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_image',
            field=models.ImageField(blank=True, null=True, upload_to='user_images'),
        ),
    ]
