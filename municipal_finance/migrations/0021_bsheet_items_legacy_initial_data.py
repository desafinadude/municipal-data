# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tablib

from django.db import migrations, models

from ..resources import BsheetItemsLegacyResource


def import_initial_data(apps, schema_editor):
    dataset = tablib.Dataset().load(
        open('municipal_finance/fixtures/initial/bsheet_items_legacy.csv')
    )
    BsheetItemsLegacyResource().import_data(dataset, raise_errors=True)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0020_financial_position_items_mscoa_initial_data'),
    ]

    operations = [
        migrations.RunPython(import_initial_data)
    ]
