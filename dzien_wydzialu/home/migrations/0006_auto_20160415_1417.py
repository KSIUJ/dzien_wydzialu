# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-15 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20160415_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='info',
            field=models.TextField(blank=True, max_length=3000),
        ),
    ]
