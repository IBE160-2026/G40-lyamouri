"""The worksheet «Slik er tallene regnet ut» (Story 2.9).

FR-7, FR-10, FR-12, FR-15, FR-16, FR-35, R-9, AD-3, AD-4, UX-DR28 to UX-DR30, UX-DR42.
The expected figures are read from the reference spreadsheet for every example that states
them, so no expected value is copied into the tests (AD-17); the sentences of the Message
Catalogue are written out, as the catalogue fixes them. The tests use no database.
"""

import dataclasses

import answer_key_reader as reader
import pytest

from explanation import worksheet
from forecasting import display
from forecasting import forecast as core
from forecasting.settings import ForecastSettings
from forecasting.weeks import Week

# The latest data week of the tests: week 45 of 2026, so horizon week 1 is week 46.
LATEST = (2026, 45)
CASES = {row["case"]: row for row in reader.cases()}
# The examples without seasonal adjustment that state a base forecast.
FORECAST_CASES = [
    name
    for name, row in CASES.items()
    if "base_forecast_shown" in row and row["seasonal_adjustment"] == "off"
]


def result_of(case, stock_on_hand=None, **changes):
    """The result of a workbook case, with a setting or the stock changed when asked."""
    row = CASES[case]
    settings = ForecastSettings(
        method=row["method"],
        window=row["window"],
        smoothing_factor=row["smoothing_factor"],
        unusual_weeks_included=row["unusual_weeks_setting"] == "included",
        scenario_percentage=row["scenario_percentage"],
        safety_margin=row["safety_margin"],
    )
    return core.forecast_product(
        [Week(w.units_sold, w.stockout) for w in row["sales"]],
        row["stock_on_hand"] if stock_on_hand is None else stock_on_hand,
        dataclasses.replace(settings, **changes),
    )


def sheet_of(case, latest=LATEST, **changes):
    return worksheet.worksheet_texts(result_of(case, **changes), *latest)


def sheet_of_units(units, stockouts=(), latest=LATEST, stock_on_hand=0, **changes):
    weeks = [Week(sold, number in stockouts) for number, sold in enumerate(units, 1)]
    settings = dataclasses.replace(ForecastSettings(), **changes)
    result = core.forecast_product(weeks, stock_on_hand, settings)
    return worksheet.worksheet_texts(result, *latest)


def tags_of(sheet):
    """The words of the tags of each week, by week label."""
    return {column.week: [tag.text for tag in column.tags] for column in sheet.sales}


# The calculation: FR-35, R-9, UX-DR29.


@pytest.mark.parametrize("case", FORECAST_CASES)
def test_the_forecast_line_ends_with_the_base_forecast_of_the_spreadsheet(case):
    """FR-35, R-9 (E1, E2, E20): the line ends with the base forecast the
    spreadsheet shows, whichever method and setting the example states."""
    calculation = sheet_of(case).calculation
    if calculation is None:  # an example without a forecast has no line
        assert CASES[case]["base_forecast_shown"] == display.MISSING
        return
    assert calculation.formula.endswith(f"= {CASES[case]['base_forecast_shown']}")


def test_the_moving_average_line_shows_its_values_and_the_weeks_used():
    """FR-35, UX-DR29 (E1): the values of the last three calculation weeks and their weeks."""
    calculation = sheet_of("E1").calculation

    assert (
        calculation.formula
        == "Glidende gjennomsnitt, 3 uker: (16 + 12 + 15) / 3 = 14,3"
    )
    assert calculation.used == "Uker brukt: uke 43, 44 og 45."
    assert calculation.rounding_note is None
    assert calculation.levels == ()


def test_exponential_smoothing_shows_its_last_update_the_note_and_every_level():
    """FR-35, R-9 (E2): the last update from the previous level, the rounding note, and a
    table of every calculation week with its sales and its level from the spreadsheet."""
    calculation = sheet_of("E2").calculation
    row = CASES["E2"]

    assert calculation.formula == (
        "Eksponentiell glatting, faktor 0,3: 0,3 × 15 + 0,7 × 13,3 = 13,8"
    )
    assert calculation.rounding_note == "Tallene er avrundet for visning."
    assert calculation.used is None
    assert [level.level for level in calculation.levels] == [
        display.one_decimal(level) for level in row["levels"]
    ]
    assert [level.units for level in calculation.levels] == [
        str(week.units_sold) for week in row["sales"]
    ]


def test_exponential_smoothing_skips_the_stockout_weeks_in_its_table():
    """R-1, R-4 (E17): a stockout week is no row of the table, as it is no level."""
    row = CASES["E17"]
    calculation = sheet_of("E17").calculation

    assert [level.units for level in calculation.levels] == ["20", "22", "21", "23"]
    assert [level.level for level in calculation.levels] == [
        display.one_decimal(level) for level in row["levels"]
    ]
    assert calculation.left_out == "Holdt utenfor: uke 42 og 43 (utsolgt)."


def test_the_smoothing_factor_and_its_complement_are_written_with_one_decimal():
    """FR-35, R-9: 1 − 0.9 is 0,1 and not 0,09999999999999998."""
    formula = sheet_of("E2", smoothing_factor=0.9).calculation.formula

    assert formula.startswith("Eksponentiell glatting, faktor 0,9: 0,9 × 15 + 0,1 × ")


# The weeks left out and the weeks used: FR-15, FR-16, UX-DR42.


def test_stockout_weeks_are_listed_with_their_reason():
    """FR-15 (E7): «Holdt utenfor: uke 42 og 43 (utsolgt).» for the stockout weeks."""
    calculation = sheet_of("E7").calculation

    assert calculation.left_out == "Holdt utenfor: uke 42 og 43 (utsolgt)."
    assert calculation.used_count is None


def test_a_stockout_week_and_an_excluded_unusual_week_are_listed_together():
    """FR-15, FR-16 (E19, setting «holdes utenfor»): stockout weeks first, each kind in time
    order, and the number of weeks used is stated."""
    calculation = sheet_of("E19 (excluded)").calculation

    assert (
        calculation.left_out
        == "Holdt utenfor: uke 42 og 43 (utsolgt), uke 44 (uvanlig)."
    )
    assert calculation.used == "Uker brukt: uke 40, 41 og 45."
    assert calculation.used_count == "3 uker brukt i beregningen."


def test_unusual_weeks_taken_into_the_calculation_are_not_left_out():
    """FR-16 (E19, setting «tas med»): only the stockout weeks are listed and no count."""
    calculation = sheet_of("E19 (included)").calculation

    assert calculation.left_out == "Holdt utenfor: uke 42 og 43 (utsolgt)."
    assert calculation.used_count is None


def test_a_level_shift_is_never_left_out():
    """FR-17, R-11 (E9, setting «holdes utenfor»): the level-shift weeks stay in."""
    calculation = sheet_of("E9 (excluded)").calculation

    assert calculation.left_out is None
    assert calculation.used_count is None
    assert calculation.used == "Uker brukt: uke 43, 44 og 45."


def test_the_list_carries_the_year_on_every_week_when_one_is_before_the_recent_period():
    """UX-DR42: a list that reaches before the last 12 weeks writes the year on all its
    weeks, also those in the recent period, and the decision is the list's."""
    units = [10] * 30
    sheet = sheet_of_units(units, stockouts=(3, 29))

    # Position 30 is week 45 of 2026, so position 3 is week 18 and position 29 week 44.
    assert (
        sheet.calculation.left_out == "Holdt utenfor: uke 18/2026 og 44/2026 (utsolgt)."
    )


def test_a_list_inside_the_recent_period_has_no_year():
    """UX-DR42: the same weeks without one before the recent period carry no year."""
    sheet = sheet_of_units([10] * 30, stockouts=(25, 29))

    assert sheet.calculation.left_out == "Holdt utenfor: uke 40 og 44 (utsolgt)."


def test_the_first_week_of_a_new_year_always_has_its_year():
    """UX-DR42: week 1 of 2027 carries the year in a list that is otherwise recent."""
    sheet = sheet_of_units([10] * 6, stockouts=(3, 4), latest=(2027, 3))

    # Positions 3 and 4 are weeks 53 of 2026 (a year with 53 weeks) and 1 of 2027.
    assert sheet.calculation.left_out == "Holdt utenfor: uke 53 og 1/2027 (utsolgt)."


def test_the_weeks_used_may_reach_before_the_recent_period_and_then_have_years():
    """UX-DR42: with stockouts in the recent period, the weeks used lie further back."""
    sheet = sheet_of_units([10] * 20, stockouts=tuple(range(10, 21)))

    assert sheet.calculation.used == "Uker brukt: uke 32/2026, 33/2026 og 34/2026."


# The sales table and its tags: FR-15 to FR-17, UX-DR28, UX-DR30.


def test_a_history_of_more_than_12_weeks_shows_the_last_12():
    """UX-DR28: «siste 12 uker» and 12 columns, oldest first."""
    sheet = sheet_of_units([10] * 30)

    assert sheet.sales_heading == "Salgshistorikk, siste 12 uker"
    assert [column.week for column in sheet.sales] == [str(n) for n in range(34, 46)]


@pytest.mark.parametrize("length", [3, 12])
def test_a_history_of_12_weeks_or_fewer_shows_all_the_weeks(length):
    """UX-DR28: «alle ukene» up to and including 12 weeks."""
    sheet = sheet_of_units([10] * length)

    assert sheet.sales_heading == "Salgshistorikk, alle ukene"
    assert len(sheet.sales) == length


def test_the_sales_table_shows_the_units_of_every_week_also_a_stockout_week():
    """FR-15: the stockout week is shown with the units it had, and is not used."""
    sheet = sheet_of("E7")

    assert [column.units for column in sheet.sales] == [
        "20",
        "22",
        "0",
        "0",
        "21",
        "23",
    ]
    assert tags_of(sheet)["42"] == ["utsolgt"]


def test_the_weeks_used_by_the_moving_average_are_the_last_n_calculation_weeks():
    """UX-DR30 (E7): «brukt» on the last three calculation weeks, never a stockout week."""
    tags = tags_of(sheet_of("E7"))

    assert [week for week, words in tags.items() if "brukt" in words] == [
        "41",
        "44",
        "45",
    ]
    assert tags["42"] == tags["43"] == ["utsolgt"]


def test_every_calculation_week_is_used_by_exponential_smoothing():
    """UX-DR30 (E17): «brukt» on all four calculation weeks."""
    tags = tags_of(sheet_of("E17"))

    assert [week for week, words in tags.items() if "brukt" in words] == [
        "40",
        "41",
        "44",
        "45",
    ]


def test_an_unusual_week_in_the_calculation_and_one_left_out_are_told_apart():
    """FR-16, NFR-7, UX-DR30 (E8): «uvanlig» when the setting takes the weeks in, and
    «uvanlig, holdt utenfor» when it leaves them out, in other words, shape and kind."""
    taken = sheet_of("E8 (included)")
    left_out = sheet_of("E8 (excluded)")
    unusual = CASES["E8 (included)"]["unusual_weeks"]
    assert unusual == [4, 5]

    for column in taken.sales[3:5]:
        tag = column.tags[0]
        assert (tag.text, tag.kind, tag.shape) == ("uvanlig", "unusual", "triangle")
    for column in left_out.sales[3:5]:
        tag = column.tags[0]
        assert (tag.text, tag.kind, tag.shape) == (
            "uvanlig, holdt utenfor",
            "unusual-out",
            "triangle-outline",
        )
    # Only the one that is taken in can also be used, and the other is never used.
    assert [t.text for t in taken.sales[3].tags] == ["uvanlig", "brukt"]
    assert [t.text for t in left_out.sales[3].tags] == ["uvanlig, holdt utenfor"]


def test_each_kind_of_tag_has_its_own_shape_and_words():
    """NFR-7, UX-DR30: no two kinds share a shape or the words, so colour is never alone."""
    kinds = worksheet.SHAPES.keys()

    assert set(kinds) == set(worksheet.WORDS)
    assert len(set(worksheet.WORDS.values())) == len(kinds)
    shapes = [shape for shape in worksheet.SHAPES.values() if shape]
    assert len(set(shapes)) == len(shapes) == len(kinds) - 1  # «brukt» has none


def test_a_level_shift_is_tagged_with_its_own_words_and_stays_used():
    """FR-17, UX-DR30 (E9): «nytt nivå» beside «brukt», whatever the setting."""
    for case in ("E9 (included)", "E9 (excluded)"):
        tags = tags_of(sheet_of(case))
        assert tags["43"] == tags["44"] == tags["45"] == ["nytt nivå", "brukt"]


def test_the_tags_follow_the_positions_of_the_spreadsheet():
    """FR-15 to FR-17 (E8, E9, E15, E16, E19): the unusual, level-shift and stockout weeks
    of the spreadsheet's rule test products are exactly the weeks with the tags."""
    products = {row["product"]: row for row in reader.products()}
    for name in ("E8", "E9", "E15", "E16", "E19"):
        row = products[name]
        result = core.forecast_product(
            [Week(w.units_sold, w.stockout) for w in row["sales"]],
            row["stock_on_hand"],
            ForecastSettings(),
        )
        sheet = worksheet.worksheet_texts(result, *LATEST)
        offset = len(row["sales"]) - len(sheet.sales)
        by_position = {
            position: [tag.text for tag in column.tags]
            for position, column in enumerate(sheet.sales, start=1 + offset)
        }
        assert {p for p, words in by_position.items() if "uvanlig" in words} == set(
            row["unusual_weeks"]
        ), name
        assert {p for p, words in by_position.items() if "nytt nivå" in words} == set(
            row["level_shift_weeks"]
        ), name
        assert {p for p, words in by_position.items() if "utsolgt" in words} == {
            number for number, week in enumerate(row["sales"], 1) if week.stockout
        }, name


def test_the_sentence_below_the_table_follows_the_mockup():
    """UX-DR28: with unusual weeks taken in, as the mockup's Strøsand 25 kg has it, the
    sentence names the weeks used, the stockout weeks and the unusual week."""
    sheet = sheet_of_units(
        [11, 13, 12, 14, 0, 2, 13, 15, 31, 16, 12, 15], stockouts=(5, 6)
    )

    assert sheet.tag_sentence == (
        "«Brukt» viser de 3 ukene i glidende gjennomsnitt. "
        "Uke 38 og 39 er utsolgte uker og er holdt utenfor beregningen. "
        "Uke 42 er en uvanlig uke og er tatt med, fordi innstillingen er «tas med»."
    )


def test_the_sentence_has_a_variant_for_each_method_setting_and_number():
    """UX-DR28: exponential smoothing, singular and plural, an excluded setting and a level shift."""
    smoothing = sheet_of("E2").tag_sentence
    assert smoothing == "«Brukt» viser alle beregningsukene i eksponentiell glatting."

    one_stockout = sheet_of("E11 a").tag_sentence
    assert one_stockout == "Uke 44 er en utsolgt uke og er holdt utenfor beregningen."

    excluded = sheet_of("E8 (excluded)").tag_sentence
    assert excluded.endswith(
        "Uke 43 og 44 er uvanlige uker og er holdt utenfor, fordi innstillingen er "
        "«holdes utenfor»."
    )
    shift = sheet_of("E9 (included)").tag_sentence
    assert shift.endswith(
        "Uke 43, 44 og 45 er nytt nivå og er alltid tatt med i beregningen."
    )


def test_a_sentence_names_only_the_tags_that_the_table_shows():
    """UX-DR28: no sentence for a kind of week that is not among the shown weeks."""
    assert sheet_of_units([10] * 5, stockouts=()).tag_sentence == (
        "«Brukt» viser de 3 ukene i glidende gjennomsnitt."
    )


# Scenarios: FR-7, FR-10, UX-DR28.


def test_the_scenario_rows_match_the_spreadsheet():
    """FR-10 (E3, E21, E23): each value the spreadsheet states for the optimistic, normal
    and pessimistic scenario is in its row, in all three horizon weeks."""
    stated = 0
    for case in ("E3", "E21", "E23"):
        row = CASES[case]
        rows = sheet_of(case).scenarios.rows
        assert [r.label for r in rows] == ["Optimistisk", "Normal", "Pessimistisk"]
        assert [r.normal for r in rows] == [False, True, False]
        for scenario_row, name in zip(
            rows, ("optimistic", "normal", "pessimistic"), strict=True
        ):
            if name in row:
                stated += 1
                assert scenario_row.values == (display.one_decimal(row[name]),) * 3, (
                    case
                )
    assert stated == 3 + 1 + 3  # E3 states all, E21 the normal one, E23 all


def test_the_columns_name_the_horizon_weeks():
    """FR-7, UX-DR42: «Uke 1 · uke 46» to «Uke 3 · uke 48»."""
    assert sheet_of("E3").scenarios.columns == (
        "Uke 1 · uke 46",
        "Uke 2 · uke 47",
        "Uke 3 · uke 48",
    )


def test_the_columns_carry_the_year_at_new_year():
    """UX-DR42: week 53 of 2026 is followed by week 1 of 2027, which has its year."""
    columns = sheet_of("E3", latest=(2026, 52)).scenarios.columns

    assert columns == ("Uke 1 · uke 53", "Uke 2 · uke 1/2027", "Uke 3 · uke 2")


def test_the_scenario_sentence_has_the_actual_percentage():
    """FR-10: «10 %» with a no-break space, and the stated percentage, not a fixed one."""
    text = sheet_of("E3").scenarios.text
    assert text == (
        "Scenarioene viser hva som skjer hvis salget blir 10 % høyere eller lavere. "
        "De er ikke sannsynligheter."
    )
    changed = sheet_of("E3", scenario_percentage=25).scenarios.text
    assert "25 % høyere" in changed


def test_the_note_says_that_weeks_2_and_3_repeat_week_1():
    """FR-7: the note without seasonal adjustment, with the catalogue's «Merknad:»."""
    assert sheet_of("E3").scenarios.note == (
        "Merknad: Uke 2 og 3 viser samme tall som uke 1 fordi metoden ikke tar hensyn til "
        "trend eller sesong."
    )


# The order calculation: FR-11, FR-12, R-8, R-9, UX-DR29.


def test_the_order_line_of_e4():
    """FR-12 (E4): the forecast, the margin as a percentage and an amount, the stock, the
    unrounded result and the suggested quantity."""
    order = sheet_of("E4").order

    assert order.line == (
        "Prognose 14,3 + sikkerhetsmargin 10 % (1,4) − lager 5 = 10,77 "
        "→ foreslått bestillingsmengde 11"
    )
    assert order.rounding_note == "Tallene er avrundet for visning."
    assert order.margin_note == (
        "Sikkerhetsmarginen er en enkel tommelfingerregel. Leveringstid og varer som "
        "allerede er bestilt, er ikke tatt med."
    )


def test_the_order_line_of_e6_says_that_the_stock_covers_the_need():
    """FR-12 (E6): a negative unrounded result is written with the minus sign, and the
    quantity 0 ends with «(lageret dekker behovet)»."""
    line = sheet_of("E6").order.line

    assert line.endswith(
        "= −40,00 → foreslått bestillingsmengde 0 (lageret dekker behovet)"
    )


def test_the_order_line_of_e21_rounds_up_to_one():
    """FR-12, R-9 (E21): 0,07 shown, and the quantity rounded up to 1."""
    line = sheet_of("E21").order.line

    assert line.endswith("= 0,07 → foreslått bestillingsmengde 1")
    assert "dekker" not in line


def test_the_order_line_of_e5_is_70_and_not_71():
    """R-9 (E5): the intermediate rounding gives 70."""
    assert sheet_of("E5").order.line.endswith(
        "= 70,00 → foreslått bestillingsmengde 70"
    )


def test_the_order_line_ends_with_the_quantity_of_the_spreadsheet():
    """FR-11, FR-12: for every example that states a quantity, the line ends with it."""
    cases = [
        name
        for name, row in CASES.items()
        if row.get("suggested_order_quantity") is not None
        and row["seasonal_adjustment"] == "off"
        and "stock_on_hand" in row
    ]
    assert {"E4", "E5", "E6", "E21", "E23"} <= set(cases)
    for case in cases:
        order = sheet_of(case).order
        assert order is not None, case
        expected = CASES[case]["suggested_order_quantity"]
        assert f"foreslått bestillingsmengde {expected}" in order.line, case


def test_a_product_with_no_stock_and_no_sales_does_not_claim_that_the_stock_covers():
    """FR-14, E23: quantity 0 with no stock has no «(lageret dekker behovet)»."""
    line = sheet_of("E23").order.line

    assert line.endswith("foreslått bestillingsmengde 0")


def test_the_safety_margin_is_the_week_1_forecast_times_the_margin():
    """R-8: the amount follows the setting, and only week 1 is read."""
    line = sheet_of("E4", safety_margin=50).order.line

    assert "sikkerhetsmargin 50 % (7,2)" in line


# No forecast and no sales: FR-8, UX-DR10.


@pytest.mark.parametrize("case", ["E11 a", "E11 b"])
def test_a_product_without_a_forecast_has_only_the_sales_table(case):
    """FR-8, UX-DR10 (E11 a and b): no calculation, no scenarios and no order line."""
    sheet = sheet_of(case)

    assert sheet.sales
    assert sheet.calculation is sheet.scenarios is sheet.order is None
    assert sheet.no_sales is None
    assert all("brukt" not in tags for tags in tags_of(sheet).values())


def test_a_product_without_sales_weeks_says_so():
    """FR-8: no table, and the page needs no week for it."""
    result = core.forecast_product([], 3, ForecastSettings())
    sheet = worksheet.worksheet_texts(result, None, None)

    assert sheet.sales == ()
    assert sheet.no_sales == "Produktet har ingen salgsuker."
    assert sheet.calculation is sheet.scenarios is sheet.order is None


# The sentence below the table names only what the table shows (review of Story 2.9).


def test_the_sentence_leaves_out_a_flagged_week_before_the_shown_weeks():
    """UX-DR28, UX-DR42: a stockout week before the last 12 weeks is in the list of weeks
    left out, with the year, but the sentence below the table names only week 44."""
    sheet = sheet_of_units([10] * 30, stockouts=(3, 29))

    assert sheet.tag_sentence == (
        "«Brukt» viser de 3 ukene i glidende gjennomsnitt. "
        "Uke 44 er en utsolgt uke og er holdt utenfor beregningen."
    )
    assert "18" not in sheet.tag_sentence
    assert "Uke 18/2026" in sheet.calculation.left_out.replace("uke", "Uke")


def test_the_sentence_has_no_used_part_when_no_used_week_is_shown():
    """UX-DR30: the weeks used lie before the shown weeks when the recent ones are
    stockout weeks, so no «brukt» tag is on the table and the sentence does not explain one."""
    sheet = sheet_of_units([10] * 20, stockouts=tuple(range(8, 21)))

    assert all("brukt" not in words for words in tags_of(sheet).values())
    assert "Brukt" not in sheet.tag_sentence
    assert sheet.calculation.used == "Uker brukt: uke 30/2026, 31/2026 og 32/2026."


def test_a_product_without_a_forecast_makes_no_claim_about_a_calculation():
    """FR-8, UX-DR10 (E11 b): unusual weeks are named without «tatt med» or «holdt
    utenfor, fordi innstillingen er …», since no calculation exists to take them into."""
    sheet = sheet_of("E11 b")

    assert sheet.calculation is None
    assert sheet.tag_sentence == "Uke 37 og 41 er uvanlige uker."
    assert "beregningen" not in sheet.tag_sentence


def test_a_level_shift_without_a_forecast_is_named_without_the_calculation():
    """FR-8, FR-17: «nytt nivå» without «alltid tatt med i beregningen»."""
    sheet = sheet_of_units([20, 22, 21, 50, 52, 51], stockouts=(), window=12)

    assert sheet.calculation is None
    assert sheet.tag_sentence == "Uke 43, 44 og 45 er nytt nivå."


# Exponential smoothing with a long history and with unusual weeks left out.


def test_the_level_table_carries_the_year_when_the_calculation_weeks_reach_back():
    """UX-DR42, FR-35: the weeks of the table of levels follow the year rule of the list."""
    sheet = sheet_of_units([10] * 20, stockouts=(5, 6), method="exponential_smoothing")

    weeks = [row.week for row in sheet.calculation.levels]
    assert len(weeks) == 18
    assert weeks[0] == "26/2026" and weeks[-1] == "45/2026"
    assert all("/2026" in week for week in weeks)


def test_the_level_table_has_no_year_when_every_calculation_week_is_recent():
    """UX-DR42: with only recent weeks, the cells are bare week numbers."""
    sheet = sheet_of_units([10] * 8, method="exponential_smoothing")

    assert [row.week for row in sheet.calculation.levels] == [
        str(number) for number in range(38, 46)
    ]


def test_exponential_smoothing_skips_the_unusual_weeks_left_out_and_counts_the_rest():
    """FR-16, FR-35 (E19, setting «holdes utenfor»): the table has no row for the unusual
    week, and the count is the number of calculation weeks."""
    sheet = sheet_of("E19 (excluded)", method="exponential_smoothing")
    calculation = sheet.calculation

    assert [row.units for row in calculation.levels] == ["40", "10", "10", "10"]
    assert calculation.used_count == "4 uker brukt i beregningen."
    assert (
        calculation.left_out
        == "Holdt utenfor: uke 42 og 43 (utsolgt), uke 44 (uvanlig)."
    )


def test_a_list_of_weeks_needs_at_least_one_week():
    """FR-15: the phrase never loses its number, so an empty list is refused."""
    with pytest.raises(ValueError, match="at least one week"):
        display.week_list([])
