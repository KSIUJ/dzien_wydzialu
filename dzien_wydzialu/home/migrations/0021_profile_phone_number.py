# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-05 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_surveyanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
    ]
