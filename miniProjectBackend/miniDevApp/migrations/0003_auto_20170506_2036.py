# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniDevApp', '0002_auto_20170506_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottleinfo',
            name='bottleId',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
        ),
    ]
