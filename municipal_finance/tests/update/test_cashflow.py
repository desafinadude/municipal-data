import csv

from django.test import TestCase
from django.core.files import File
from django.contrib.auth.models import User

from municipal_finance.models import CashflowUpdate, CflowFacts, CflowItems
from municipal_finance.update import update_cashflow

FIXTURES_PATH = 'municipal_finance/fixtures/fiscal_update/cashflow'
CASHFLOW_ITEM_FIELDNAMES = [
    'code',
    'label',
    'position_in_return_form',
    'return_form_structure',
    'composition',
]


class UpdateCashflowTestCase(TestCase):
    def setUp(self):
        # Load items into the database
        with open(f'{FIXTURES_PATH}/items.csv') as f:
            reader = csv.DictReader(
                f, delimiter=',', fieldnames=CASHFLOW_ITEM_FIELDNAMES)
            for row in reader:
                row = {k: None if not v else v for k, v in row.items()}
                CflowItems.objects.create(**row)
        # Create test user
        self.user = User.objects.create_user(
            username="sample", email="sample@some.co", password="testpass",
        )
        # Create initial upload to process
        self.initial_upload = CashflowUpdate.objects.create(
            user=self.user,
            file=File(open(f'{FIXTURES_PATH}/initial.csv', 'rb')),
        )

    def test_initial(self):
        result = update_cashflow(self.initial_upload)
        records = CflowFacts.objects.all()
        self.assertEquals(result, {"updated": 0, "created": 2})
        self.assertQuerysetEqual(records, [repr(o) for o in [
            CflowFacts(
                id=1,
                demarcation_code='BUF',
                period_code='2018AUDA',
                item_code_id='0430',
                amount=1747525755,
                amount_type_code='AUDA',
                financial_year='2018',
                period_length='year',
                financial_period='2018',
            ),
            CflowFacts(
                id=1,
                demarcation_code='BUF',
                period_code='2019AUDA',
                item_code_id='0430',
                amount=1823063888,
                amount_type_code='AUDA',
                financial_year='2019',
                period_length='year',
                financial_period='2019',
            ),
        ]], ordered=False)
