import csv

from django.test import TransactionTestCase
from django.core.files import File
from django.contrib.auth.models import User

from municipal_finance.compile.profile import compile_profile
from municipal_finance.update import update_cashflow
from municipal_finance.models import CashflowUpdate, CflowFacts, CflowItems

FIXTURES_PATH = 'municipal_finance/fixtures/fiscal_update/cashflow'
CASHFLOW_ITEM_FIELDNAMES = [
    'code',
    'label',
    'position_in_return_form',
    'return_form_structure',
    'composition',
]


class CompileProfileTestCase(TransactionTestCase):
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
            username='sample', email='sample@some.co', password='testpass',
        )
        # Create initial upload to process
        self.initial_upload = CashflowUpdate.objects.create(
            user=self.user,
            file=File(open(f'{FIXTURES_PATH}/initial.csv', 'rb')),
        )
        # Process initial upload
        update_cashflow(self.initial_upload)

    def test_compile(self):
        result = compile_profile('BUF', 2019)
        print(result)
