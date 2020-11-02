# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tablib

from django.db import migrations, models

from ..resources import AmountTypeMSCOAResource


def import_initial_data(apps, schema_editor):
    dataset = tablib.Dataset().load(
        open('municipal_finance/fixtures/initial/amount_type_mscoa.csv')
    )
    AmountTypeMSCOAResource().import_data(dataset, raise_errors=True)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_finance', '0013_auto_20201102_1538'),
    ]

    operations = [
        migrations.RunPython(import_initial_data)
    ]
