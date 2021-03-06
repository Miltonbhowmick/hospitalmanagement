# Generated by Django 3.0 on 2020-12-10 11:34

import ckeditor.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20201210_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodBlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=255)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime(2020, 12, 10, 17, 34, 37, 744020))),
                ('post_image', models.ImageField(blank=True, null=True, upload_to='blog_images')),
                ('description', ckeditor.fields.RichTextField(blank=True, max_length=1000, null=True)),
                ('view', models.IntegerField(blank=True, default=0)),
                ('slug', models.SlugField(blank=True, default='', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FoodBlogView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=40)),
                ('session', models.CharField(blank=True, max_length=40)),
                ('created', models.DateTimeField(default=datetime.datetime(2020, 12, 10, 17, 34, 37, 745045))),
                ('foodblog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foodblog', to='home.FoodBlog')),
            ],
        ),
    ]
