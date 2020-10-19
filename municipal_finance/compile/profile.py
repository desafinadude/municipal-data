from django.conf import settings
from sqlalchemy import create_engine

from ..cubes import PreloadingJSONCubeManager


YEAR_ITEM_DRILLDOWN = [
    'item.code',
    'financial_year_end.year',
]


def get_manager():
    config = settings.DATABASES['default']
    url = f"postgres://{config['USER']}:{config['PASSWORD']}@{config['HOST']}/{config['NAME']}"
    # url = settings.DATABASE_URL
    engine = create_engine(url)
    return (engine, PreloadingJSONCubeManager(engine, 'models/mscoa'),)


def format_cut_params(cuts):
    keypairs = []
    for key, vals in cuts.items():
        vals_as_strings = []
        for val in vals:
            if type(val) == str:
                vals_as_strings.append('"' + val + '"')
            if type(val) == int:
                vals_as_strings.append(str(val))
        keypairs.append((key, ";".join(vals_as_strings)))
    return "|".join("{!s}:{!s}".format(pair[0], pair[1]) for pair in keypairs)


def compile_profile(demarcation_code, last_year):
    years = list(range(last_year - 3, last_year + 1))
    years.reverse()
    engine, manager = get_manager()
    cube = manager.get_cube('cashflow')
    cuts = format_cut_params({
        'item.code': ['0430'],
        'amount_type.code': ['AUDA'],
        'demarcation.code': [demarcation_code],
        'period_length.length': ['year'],
        'financial_year_end.year': years,
    })
    import pdb
    pdb.set_trace()
    result = cube.aggregate(
        aggregates='amount.sum',
        drilldowns='item.code|financial_year_end.year',
        cuts=cuts,
        order='financial_year_end.year:desc,item.code:asc',
        page=0,
        page_size=20000,
        page_max=20000,
    )
    engine.dispose()
    return result
