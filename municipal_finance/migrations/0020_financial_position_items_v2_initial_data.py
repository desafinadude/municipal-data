# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tablib

from django.db import migrations, models

from ..resources import FinancialPositionItemsV2Resource


def import_initial_data(apps, schema_editor):
    dataset = tablib.Dataset().load(
        open('municipal_finance/fixtures/initial/financial_position_items_v2.csv')
    )
    FinancialPositionItemsV2Resource().import_data(dataset, raise_errors=True)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0019_auto_20201103_0744'),
    ]

    operations = [
        migrations.RunPython(import_initial_data)
    ]
