# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-03-11 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('household', '0009_auto_20200310_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialyear',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
