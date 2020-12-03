
from .indicator_calculator import IndicatorCalculator
from .utils import (
    ratio,
    group_amount_by_year,
    filter_for_all_keys,
    populate_periods,
)


def determine_rating(result):
    if result > 3:
        return "good"
    elif result <= 1:
        return "bad"
    else:
        return "ave"


def generate_data(year, values):
    data = {
        "date": year,
    }
    if values:
        cash_at_year_end = values["cash_at_year_end"]
        monthly_expenses = values["operating_expenditure"] / 12
        calculated_ratio = ratio(cash_at_year_end, monthly_expenses, 1)
        result = max(calculated_ratio, 0)
        data.update({
            "result": result,
            "rating": determine_rating(result),
        })
    else:
        data.update({
            "result": None,
            "rating": None,
        })
    return data


class CashCoverage(IndicatorCalculator):
    indicator_name = "cash_coverage"
    result_type = "months"
    noun = "coverage"
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        results = api_data.results
        periods = {}
        # Populate periods with v1 data
        populate_periods(
            periods,
            group_amount_by_year(results["cash_flow_v1"]),
            "cash_at_year_end",
        )
        populate_periods(
            periods,
            group_amount_by_year(results["operating_expenditure_actual_v1"]),
            "operating_expenditure",
        )
        # Populate periods with v2 data
        populate_periods(
            periods,
            group_amount_by_year(results["cash_flow_v2"]),
            "cash_at_year_end",
        )
        populate_periods(
            periods,
            group_amount_by_year(results["operating_expenditure_actual_v2"]),
            "operating_expenditure",
        )
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys(periods, [
            "cash_at_year_end", "operating_expenditure",
        ])
        # Convert periods into dictionary
        periods = dict(periods)
        # Generate data for the requested years
        values = list(
            map(
                lambda year: generate_data(year, periods.get(year)),
                api_data.years,
            )
        )
        # Return the compiled data
        return {
            "values": values,
            "ref": api_data.references["solgf"],
        }
