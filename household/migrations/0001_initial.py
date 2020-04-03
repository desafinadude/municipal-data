# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-03-03 13:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('scorecard', '0003_geography_population'),
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetPhase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget_year', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='HouseholdBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_vat', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('budget_phase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='household.BudgetPhase')),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='household.FinancialYear')),
                ('geography', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scorecard.Geography')),
            ],
        ),
        migrations.CreateModel(
            name='HouseholdClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='HouseholdIncrease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.FloatField()),
                ('budget_phase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='household.BudgetPhase')),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='household.FinancialYear')),
                ('geography', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scorecard.Geography')),
                ('household_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='household.HouseholdClass')),
            ],
        ),
        migrations.CreateModel(
            name='HouseholdService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='householdbill',
            name='household_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='household.HouseholdClass'),
        ),
        migrations.AddField(
            model_name='householdbill',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='household.HouseholdService'),
        ),
        migrations.AlterUniqueTogether(
            name='householdbill',
            unique_together=set([('financial_year', 'budget_phase', 'household_class', 'service', 'total')]),
        ),
    ]
