"""The FR-20 defaults and ranges are defined once, in forecasting/settings.py
(Story 1.7; FR-20, AD-9).

The PRD's FR-20 table is read from the PRD, so no expected value is copied into
test code. These tests need no database; the import rule of the core is checked
in test_core_imports.py, which also covers forecasting/settings.py.
"""

from decimal import Decimal

import answer_key
import answer_key_reader as reader

from forecasting import settings as defaults
from web.models import CompanySettings

NUMBER_SETTINGS = {
    "window": defaults.WINDOW,
    "smoothing_factor": defaults.SMOOTHING_FACTOR,
    "scenario_percentage": defaults.SCENARIO_PERCENTAGE,
    "safety_margin": defaults.SAFETY_MARGIN,
}


def test_the_defaults_are_the_ones_in_the_prd():
    """FR-20, AD-9: the method, the four numbers and the two switches start at the
    values of the FR-20 table."""
    expected = answer_key.prd_defaults()

    assert defaults.DEFAULT_METHOD == expected["method"]
    for column, setting in NUMBER_SETTINGS.items():
        assert setting.default == Decimal(str(expected[column])), column
    assert defaults.DEFAULT_UNUSUAL_WEEKS_INCLUDED is (
        expected["unusual_weeks_setting"] == "included"
    )
    assert defaults.DEFAULT_SEASONAL_ADJUSTMENT is (
        expected["seasonal_adjustment"] == "on"
    )


def test_the_ranges_are_the_ones_in_the_prd():
    """FR-20, AD-9: each number setting is allowed between the minimum and the
    maximum of the FR-20 table, both included, and its default lies inside."""
    expected = answer_key.prd_ranges()

    for column, setting in NUMBER_SETTINGS.items():
        assert (setting.minimum, setting.maximum) == expected[column], column
        assert setting.minimum <= setting.default <= setting.maximum, column


def test_the_methods_are_the_names_of_the_answer_key():
    """AD-9, AD-17: the two method names are those that the reference spreadsheet
    uses, so its cases can be compared with the core."""
    assert defaults.METHODS == reader.METHODS


def test_a_new_settings_row_reads_the_defaults():
    """FR-20, AD-9: a CompanySettings row made without values holds the defaults
    from forecasting/settings.py, with no second copy in the model."""
    row = CompanySettings()

    assert row.method == defaults.DEFAULT_METHOD
    assert row.window == defaults.WINDOW.default
    assert row.smoothing_factor == defaults.SMOOTHING_FACTOR.default
    assert row.scenario_percentage == defaults.SCENARIO_PERCENTAGE.default
    assert row.safety_margin == defaults.SAFETY_MARGIN.default
    assert row.unusual_weeks_included is defaults.DEFAULT_UNUSUAL_WEEKS_INCLUDED
    assert row.seasonal_adjustment is defaults.DEFAULT_SEASONAL_ADJUSTMENT


def test_the_smoothing_factor_keeps_one_decimal():
    """AD-9: the smoothing factor has one decimal, from 0,1 to 0,9, so its column
    holds two digits with one after the point."""
    field = CompanySettings._meta.get_field("smoothing_factor")

    assert (field.max_digits, field.decimal_places) == (2, 1)
    assert defaults.SMOOTHING_FACTOR.default.as_tuple().exponent == -1
