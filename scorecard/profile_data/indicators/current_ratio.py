from .utils import (
    ratio,
    sum_item_amounts,
    filter_for_all_keys,
    group_items_by_year,
)
from .indicator_calculator import IndicatorCalculator


def translate_rating(value):
    if value >= 1.5:
        return "good"
    elif value >= 1:
        return "ave"
    else:
        return "bad"


def generate_data(year, values):
    data = {
        "date": year,
        "year": year,
    }
    if values:
        assets = values["assets"]
        liabilities = values["liabilities"]
        result = ratio(assets, liabilities)
        data.update({
            "amount_type": "AUDA",
            "assets": assets,
            "liabilities": liabilities,
            "result": result,
            "rating": translate_rating(result),
        })
    else:
        data.update({
            "result": None,
            "rating": "bad",
        })
    return data


class CurrentRatio(IndicatorCalculator):
    indicator_name = "current_ratio"
    result_type = "ratio"
    noun = "ratio"
    has_comparisons = True

    @classmethod
    def get_muni_specifics(cls, api_data):
        results = api_data.results
        periods = {}
        # Populate periods with v1 data
        grouped_results = group_items_by_year(results["bsheet_auda_years"])
        for key, result in grouped_results:
            periods.setdefault(key, {})
            periods[key]["assets"] = result.get("2150")
            periods[key]["liabilities"] = result.get("1600")
        # Populate periods with v2 data
        grouped_results = group_items_by_year(results["bsheet_auda_years_v2"])
        for key, result in grouped_results:
            periods.setdefault(key, {})
            periods[key]["assets"] = sum_item_amounts(result, [
                "0120", "0130", "0140", "0150", "0160", "0170",
            ])
            periods[key]["liabilities"] = sum_item_amounts(result, [
                "0330", "0340", "0350", "0360", "0370",
            ])
        # Filter out periods that don't have all the required data
        periods = filter_for_all_keys(periods, [
            "assets", "liabilities",
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
            "ref": api_data.references["circular71"],
            "result_type": cls.result_type,
        }
