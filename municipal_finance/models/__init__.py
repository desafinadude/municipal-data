# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from .amount_type import (
    AmountType,
    AmountTypeV2,
)
from .government_functions import (
    GovernmentFunctionsV1,
    GovernmentFunctionsV2,
)
from .cash_flow import (
    CflowItemsV1,
    CflowFactsV1,
    CflowItemsV2,
    CflowFactsV2,
)
from .income_expenditure import (
    IncexpItemsV1,
    IncexpFactsV1,
    IncexpItemsV2,
    IncexpFactsV2,
)
from .financial_position import (
    BsheetItemsV1,
    BsheetFactsV1,
    BsheetItemsV2,
    BsheetFactsV2,
)
from .municipality_profiles_compilation import (
    MunicipalityProfilesCompilation,
)


class AgedCreditorFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    item_code = models.ForeignKey(
        'AgedCreditorItems', models.DO_NOTHING, db_column='item_code')
    g1_amount = models.BigIntegerField(null=True)
    l1_amount = models.BigIntegerField(null=True)
    l120_amount = models.BigIntegerField(null=True)
    l150_amount = models.BigIntegerField(null=True)
    l180_amount = models.BigIntegerField(null=True)
    l30_amount = models.BigIntegerField(null=True)
    l60_amount = models.BigIntegerField(null=True)
    l90_amount = models.BigIntegerField(null=True)
    total_amount = models.BigIntegerField(null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()
    amount_type_code = models.TextField()

    class Meta:
        db_table = 'aged_creditor_facts'
        unique_together = (
            ('demarcation_code', 'period_code', 'item_code'),
            (
                'amount_type_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'item_code',
                'period_length',
            ),
        )


class AgedCreditorItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField()
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        db_table = 'aged_creditor_items'


class AgedDebtorFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    customer_group_code = models.TextField()
    item_code = models.ForeignKey(
        'AgedDebtorItems', models.DO_NOTHING, db_column='item_code')
    bad_amount = models.BigIntegerField(null=True)
    badi_amount = models.BigIntegerField(null=True)
    g1_amount = models.BigIntegerField(null=True)
    l1_amount = models.BigIntegerField(null=True)
    l120_amount = models.BigIntegerField(null=True)
    l150_amount = models.BigIntegerField(null=True)
    l180_amount = models.BigIntegerField(null=True)
    l30_amount = models.BigIntegerField(null=True)
    l60_amount = models.BigIntegerField(null=True)
    l90_amount = models.BigIntegerField(null=True)
    total_amount = models.BigIntegerField(null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()
    amount_type_code = models.TextField()

    class Meta:
        db_table = 'aged_debtor_facts'
        unique_together = (
            ('demarcation_code', 'period_code',
             'customer_group_code', 'item_code'),
            (
                'amount_type_code',
                'customer_group_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'item_code',
                'period_length',
            ),
        )


class AgedDebtorItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField()
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        db_table = 'aged_debtor_items'


class AuditOpinionFacts(models.Model):
    demarcation_code = models.TextField()
    financial_year = models.IntegerField()
    opinion_code = models.TextField()
    opinion_label = models.TextField()
    report_url = models.TextField(null=True)

    class Meta:
        db_table = 'audit_opinion_facts'


class AuditOpinions(models.Model):
    demarcation_code = models.TextField()
    financial_year = models.TextField()
    opinion_code = models.TextField()
    opinion_label = models.TextField()

    class Meta:
        db_table = 'audit_opinions'
        unique_together = (('demarcation_code', 'financial_year'),)


class CapitalFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    function_code = models.ForeignKey(
        GovernmentFunctionsV1,
        models.DO_NOTHING,
        db_column='function_code'
    )
    item_code = models.ForeignKey(
        'CapitalItems', models.DO_NOTHING, db_column='item_code')
    new_assets = models.BigIntegerField(null=True)
    renewal_of_existing = models.BigIntegerField(null=True)
    total_assets = models.BigIntegerField(null=True)
    repairs_maintenance = models.BigIntegerField(null=True)
    asset_register_summary = models.BigIntegerField(null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()
    amount_type_code = models.TextField()

    class Meta:
        db_table = 'capital_facts'
        unique_together = (
            ('demarcation_code', 'period_code', 'function_code', 'item_code'),
            (
                'amount_type_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'function_code',
                'item_code',
                'period_length',
            ),
        )


class CapitalItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField()
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        db_table = 'capital_items'


class ConditionalGrants(models.Model):
    code = models.TextField(null=True)
    name = models.TextField(null=True)

    class Meta:
        db_table = 'conditional_grants'


class ConditionalGrantsFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    grant_code = models.TextField()
    amount = models.BigIntegerField(null=True)
    amount_type_code = models.TextField()
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()

    class Meta:
        db_table = 'conditional_grants_facts'
        unique_together = (
            ('demarcation_code', 'period_code', 'grant_code'),
            (
                'amount_type_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'grant_code',
                'period_length',
            ),
        )


class MunicipalityStaffContacts(models.Model):
    id = models.AutoField(primary_key=True)
    demarcation_code = models.TextField()
    role = models.TextField()
    title = models.TextField(null=True)
    name = models.TextField(null=True)
    office_number = models.TextField(null=True)
    fax_number = models.TextField(null=True)
    email_address = models.TextField(null=True)

    class Meta:
        db_table = 'municipality_staff_contacts'
        unique_together = (('demarcation_code', 'role'),)


class MunicipalityStaffContactsUpload(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    datetime = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/contacts/')

    class Meta:
        db_table = 'municipality_staff_contacts_uploads'


class RepmaintFacts(models.Model):
    demarcation_code = models.TextField()
    period_code = models.TextField()
    item_code = models.TextField()
    amount = models.BigIntegerField(null=True)
    financial_year = models.IntegerField()
    period_length = models.TextField()
    financial_period = models.IntegerField()
    amount_type_code = models.TextField()

    class Meta:
        db_table = 'repmaint_facts'
        unique_together = (
            ('demarcation_code', 'period_code', 'item_code'),
            (
                'amount_type_code',
                'demarcation_code',
                'financial_period',
                'financial_year',
                'item_code',
                'period_length',
            ),
        )


class RepmaintItems(models.Model):
    code = models.TextField(primary_key=True)
    label = models.TextField()
    position_in_return_form = models.IntegerField(null=True)
    return_form_structure = models.TextField(null=True)
    composition = models.TextField(null=True)

    class Meta:
        db_table = 'repmaint_items'


class UifwexpFacts(models.Model):
    demarcation_code = models.TextField()
    financial_year = models.IntegerField()
    item_code = models.TextField()
    item_label = models.TextField()
    amount = models.BigIntegerField(null=True)

    class Meta:
        db_table = 'uifwexp_facts'
        unique_together = (
            ('demarcation_code', 'financial_year', 'item_code'),)


class DemarcationChanges(models.Model):
    date = models.DateField(blank=False, null=False)
    old_code = models.TextField(blank=False, null=False, db_index=True)
    new_code = models.TextField(blank=False, null=False, db_index=True)
    old_code_transition = models.TextField(
        blank=False, null=False, db_index=True)
    new_code_transition = models.TextField(
        blank=False, null=False, db_index=True)


class MunicipalityProfile(models.Model):
    demarcation_code = models.CharField(max_length=10, primary_key=True)
    data = JSONField()

    class Meta:
        db_table = 'municipality_profile'


class MedianGroup(models.Model):
    group_id = models.CharField(max_length=10, primary_key=True)
    data = JSONField()


class RatingCountGroup(models.Model):
    group_id = models.CharField(max_length=10, primary_key=True)
    data = JSONField()

# class Median(models.Model):
#     area_code = models.CharField(max_length=5)
#     miif_category = models.CharField(max_length=2)
#     indicator = models.CharField(max_length=30)
#     period = models.CharField(max_length=6)
#     value = models.FloatField()

#     class Meta:
#         unique_together = ('area_code', 'miif_category', 'indicator', 'year',)
