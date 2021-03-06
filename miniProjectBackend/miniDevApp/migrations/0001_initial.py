# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 05:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BottleInfo',
            fields=[
                ('bottleId', models.BigAutoField(default=1, primary_key=True, serialize=False)),
                ('bottleName', models.CharField(max_length=30)),
                ('bottleStatus', models.IntegerField()),
                ('bottlePrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bottleInfo', models.CharField(max_length=100)),
                ('bottleImageUrl', models.CharField(max_length=100)),
                ('sendTimestamp', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReportList',
            fields=[
                ('report_bottleId', models.BigAutoField(default=1, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('qqId', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('phoneNumber', models.CharField(max_length=20)),
                ('userAddress', models.CharField(max_length=100)),
                ('userPostion', models.CharField(max_length=100)),
                ('userImageUrl', models.CharField(max_length=100)),
                ('userNickName', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('wish_bottleId', models.BigAutoField(default=1, primary_key=True, serialize=False)),
                ('bottleStatus', models.IntegerField()),
                ('wishUserInfo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='miniDevApp.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='reportlist',
            name='qqId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='miniDevApp.UserInfo'),
        ),
        migrations.AddField(
            model_name='bottleinfo',
            name='bottleUserInfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='miniDevApp.UserInfo'),
        ),
    ]
