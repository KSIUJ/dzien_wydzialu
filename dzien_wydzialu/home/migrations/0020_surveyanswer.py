# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-05 13:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_surveycode'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(max_length=3000)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Activity')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Group')),
            ],
        ),
    ]