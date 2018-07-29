# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-27 15:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('username', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=25)),
                ('confirm', models.CharField(max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=25)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to='webapp.User')),
                ('savers', models.ManyToManyField(default=0, related_name='saved_by', to='webapp.User')),
            ],
        ),
    ]
