# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-02 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20160601_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]