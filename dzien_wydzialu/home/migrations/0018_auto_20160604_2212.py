# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 22:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20160604_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitorgroup',
            name='assigned_group',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_group', to='home.Group'),
        ),
    ]