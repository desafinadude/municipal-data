import csv
import requests
import re

from contextlib import closing

from .models import MunicipalityStaffContacts, CflowFacts


PERIOD_CODE_RE = re.compile(r'^(?P<year>[0-9]{4})(?P<code>[A-Z]{4})$')
STAFF_CONTACTS_FIELDNAMES = [
    'demarcation_code',
    'role',
    'title',
    'name',
    'office_number',
    'fax_number',
    'email_address',
]
CASHFLOW_FACT_FIELDNAMES = [
    'demarcation_code',
    'period_code',
    'item_code',
    'amount',
]


def update_municipal_staff_contacts(obj):
    # Read the file
    updated_count = 0
    created_count = 0
    with closing(requests.get(obj.file.url, stream=True)) as r:
        f = (line.decode('utf-8') for line in r.iter_lines())
        reader = csv.DictReader(f, fieldnames=STAFF_CONTACTS_FIELDNAMES)
        # TODO: Confirm column names
        # Process all the rows in the file
        for row in reader:
            if reader.line_num > 1:
                query = MunicipalityStaffContacts.objects.filter(
                    demarcation_code__exact=row['demarcation_code'],
                    role__exact=row['role'],
                )
                record = query.first()
                if record is None:
                    record = MunicipalityStaffContacts(
                        demarcation_code=row['demarcation_code'],
                        role=row['role'],
                        title=row['title'],
                        name=row['name'],
                        office_number=row['office_number'],
                        fax_number=row['fax_number'],
                        email_address=row['email_address'],
                    )
                    record.save(force_insert=True)
                    created_count += 1
                else:
                    # TODO: Determine update extent
                    query.update(
                        title=row['title'],
                        name=row['name'],
                        office_number=row['office_number'],
                        fax_number=row['fax_number'],
                        email_address=row['email_address'],
                    )
                    updated_count += 1
    return {
        "updated": updated_count,
        "created": created_count,
    }


def update_cashflow(record):
    created_count = 0
    request = requests.get(record.file.url)
    content = request.content.decode('utf-8')
    reader = csv.DictReader(content.splitlines(),
                            fieldnames=CASHFLOW_FACT_FIELDNAMES)
    for row in reader:
        match = PERIOD_CODE_RE.match(row['period_code'])
        row['amount_type_code'] = match.group('code')
        row['financial_year'] = match.group('year')
        row['period_length'] = 'year'
        row['financial_period'] = match.group('year')
        row['item_code_id'] = row['item_code']
        del row['item_code']
        CflowFacts.objects.create(**row)
        created_count += 1
    return {
        'updated': 0,
        'created': created_count,
    }
