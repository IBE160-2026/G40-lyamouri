"""The texts of the warnings, the notes and the confidence reasons (Story 2.5).

AD-4, UX-DR40, FR-7, FR-8, FR-15 to FR-19. Each expected text is the row of the EXPERIENCE.md
Message Catalogue filled from the result, and each result comes from the reference
spreadsheet or from a history built here. They use no database.
"""

import dataclasses
from pathlib import Path

import answer_key_reader as reader
import pytest

from explanation import trust as words
from forecasting import forecast as core
from forecasting import trust
from forecasting.settings import ForecastSettings
from forecasting.weeks import Week

# The latest data week of Testbedrift A (UX-DR46): position 104 is week 45 of 2026.
LATEST = (2026, 45)
CATALOGUE = (
    Path(__file__).resolve().parents[1]
    / "_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15"
    / "EXPERIENCE.md"
)
FEW_WEEKS_WARNING = (
    "Produktet har 2 gyldige uker. Prognose regner ut en prognose når produktet har "
    "minst 3 gyldige uker."
)
WINDOW_WARNING = (
    "Glidende gjennomsnitt over 12 uker trenger 12 uker brukt i beregningen. "
    "Produktet har 10."
)
FLAT_WEEKS_NOTE = (
    "Uke 2 og 3 viser samme tall som uke 1 fordi metoden ikke tar hensyn til trend "
    "eller sesong."
)


def core_weeks(sales):
    return [Week(week.units_sold, week.stockout) for week in sales]


def case_result(name, **changes):
    row = next(row for row in reader.cases() if row["case"] == name)
    settings = ForecastSettings(
        method=row["method"],
        window=row["window"],
        smoothing_factor=row["smoothing_factor"],
        unusual_weeks_included=row["unusual_weeks_setting"] == "included",
    )
    return core.forecast_product(
        core_weeks(row["sales"]),
        row["stock_on_hand"],
        dataclasses.replace(settings, **changes),
    )


def product_result(name):
    row = next(row for row in reader.products() if row["product"] == name)
    return core.forecast_product(
        core_weeks(row["sales"]), row["stock_on_hand"], ForecastSettings()
    )


def series(length, units=10, stockouts=(), spikes=None):
    spikes = spikes or {}
    return [
        Week(spikes.get(position, units), position in stockouts)
        for position in range(1, length + 1)
    ]


def forecast(weeks, settings=None):
    return core.forecast_product(weeks, 0, settings or ForecastSettings())


def texts(result, latest=LATEST):
    return [
        (warning.code, warning.text) for warning in words.warning_texts(result, *latest)
    ]


def test_strosand_has_the_texts_of_the_catalogue_and_the_reason_of_fr_19():
    """FR-15, FR-16, FR-19 (Strøsand 25 kg): weeks 38 and 39 are sold out and week 42 is
    unusual with 31 units, and the reason is the catalogue's own example."""
    result = product_result("Strøsand 25 kg")

    assert texts(result) == [
        ("stockout_weeks", "Uke 38 og 39: utsolgt, holdt utenfor beregningen."),
        (
            "unusual_weeks",
            "Uke 42: uvanlig høyt salg (31), tatt med i beregningen.",
        ),
    ]
    assert (
        words.confidence_reason(result)
        == "Middels: 2 utsolgte uker og 1 uvanlig uke de siste 12 ukene."
    )
    assert words.list_text(result) is None


def test_excluded_unusual_weeks_are_held_outside_the_calculation_in_the_text():
    """FR-16: with the setting that excludes them, the warning says so, and it is still
    there."""
    row = next(row for row in reader.products() if row["product"] == "Strøsand 25 kg")
    result = core.forecast_product(
        core_weeks(row["sales"]),
        row["stock_on_hand"],
        ForecastSettings(unusual_weeks_included=False),
    )

    assert texts(result)[1] == (
        "unusual_weeks",
        "Uke 42: uvanlig høyt salg (31), holdt utenfor beregningen.",
    )


def test_several_unusual_weeks_list_their_weeks_and_their_sales():
    """FR-16: «Uke [40 og 42]: uvanlig høyt salg ([29 og 31]), …» for several weeks."""
    result = forecast(series(104, spikes={100: 29, 102: 31}))

    assert texts(result) == [
        (
            "unusual_weeks",
            "Uke 41 og 43: uvanlig høyt salg (29 og 31), tatt med i beregningen.",
        )
    ]
    assert (
        words.confidence_reason(result) == "Middels: 2 uvanlige uker de siste 12 ukene."
    )


def test_three_or_more_weeks_are_joined_with_commas_and_og():
    """FR-15: the nine sold-out weeks of E12 read «37, 38, … og 45»."""
    result = case_result("E12 (95)")

    assert texts(result)[0] == (
        "stockout_weeks",
        "Uke 37, 38, 39, 40, 41, 42, 43, 44 og 45: utsolgt, holdt utenfor beregningen.",
    )


def test_the_first_week_of_a_new_year_carries_its_year_in_a_week_list():
    """AD-3, FR-15: weeks 53 of 2026 and 1 of 2027 in one list read «53, 1/2027 og 2»."""
    result = forecast(series(104, stockouts={102, 103, 104}))

    assert texts(result, latest=(2027, 2))[0] == (
        "stockout_weeks",
        "Uke 53, 1/2027 og 2: utsolgt, holdt utenfor beregningen.",
    )


def test_old_data_names_the_weeks_since_the_latest_valid_week():
    """FR-18, R-15 (E12): 9 weeks give the old-data warning, and the reason names the 9
    sold-out weeks first and then the old data as its own sentence."""
    result = case_result("E12 (95)")

    assert texts(result)[1] == (
        "old_data",
        "Det har gått 9 uker siden siste gyldige uke, så prognosen bygger på gamle data.",
    )
    assert words.confidence_reason(result) == (
        "Middels: 9 utsolgte uker de siste 12 ukene. "
        "Gamle data, 9 uker siden siste gyldige uke."
    )


def test_old_data_alone_is_a_phrase_of_its_own_in_the_reason():
    """FR-18, FR-19 (guard case): old data always comes with sold-out weeks in the recent
    period, so under R-15 this phrase cannot occur alone; its wording is fixed in the
    catalogue as a guard case and tested on a result built here."""
    result = dataclasses.replace(
        forecast(series(104)),
        warnings=(trust.OLD_DATA,),
        weeks_since_latest_valid=9,
        confidence_label=trust.MIDDELS,
        confidence_condition=trust.ACTIVE_WARNING,
    )

    assert (
        words.confidence_reason(result)
        == "Middels: gamle data, 9 uker siden siste gyldige uke."
    )


def test_too_few_valid_weeks_has_a_list_text_a_warning_and_a_reason():
    """FR-8, FR-24, R-16 (E11 a): 2 valid weeks and 1 sold-out week give no forecast; the
    reason names the missing forecast and then the stockout week."""
    result = case_result("E11 a")

    assert words.list_text(result) == "Ingen prognose: færre enn 3 gyldige uker"
    assert texts(result) == [
        ("stockout_weeks", "Uke 44: utsolgt, holdt utenfor beregningen."),
        (
            "insufficient_data",
            FEW_WEEKS_WARNING,
        ),
    ]
    assert words.confidence_reason(result) == (
        "Lav: ingen prognose, færre enn 3 gyldige uker. "
        "1 utsolgt uke de siste 12 ukene."
    )


@pytest.mark.parametrize(
    ("valid", "count"),
    [(0, "0 gyldige uker"), (1, "1 gyldig uke"), (2, "2 gyldige uker")],
)
def test_the_number_of_valid_weeks_has_its_singular_and_plural(valid, count):
    """FR-8: «Produktet har [1] gyldig uke.»"""
    result = forecast([Week(5, False)] * valid)

    assert f"Produktet har {count}. " in texts(result)[0][1]
    assert words.confidence_reason(result) == (
        "Lav: ingen prognose, færre enn 3 gyldige uker."
    )


def test_the_window_case_names_the_window_the_weeks_used_and_the_reason_of_e29_e():
    """FR-8, R-16 (E11 b, E29 e): 12 valid weeks of which 2 are excluded leave 10 for a
    window of 12; the reason is the catalogue's, followed by the unusual-weeks sentence."""
    result = case_result("E29 e")

    assert words.list_text(result) == "Ingen prognose: færre uker enn vinduet"
    assert texts(result) == [
        (
            "unusual_weeks",
            "Uke 37 og 41: uvanlig høyt salg (30 og 30), holdt utenfor beregningen.",
        ),
        (
            "insufficient_data",
            WINDOW_WARNING,
        ),
    ]
    assert words.confidence_reason(result) == (
        "Lav: ingen prognose, færre uker enn vinduet. "
        "2 uvanlige uker de siste 12 ukene."
    )


def test_fewer_than_12_valid_weeks_with_a_warning_names_both():
    """FR-19, R-16: «Lav: færre enn 12 gyldige uker. 1 utsolgt uke de siste 12 ukene.»"""
    result = forecast(series(11, stockouts={5}))

    assert words.list_text(result) is None
    assert words.confidence_reason(result) == (
        "Lav: færre enn 12 gyldige uker. 1 utsolgt uke de siste 12 ukene."
    )


def test_an_active_warning_with_a_short_history_names_only_the_warning():
    """R-16: the first condition decides, so the warning is named and the short history is
    not: a snapshot of a product with both."""
    result = forecast(series(80, stockouts={79}))

    assert result.confidence_condition == trust.ACTIVE_WARNING
    assert (
        words.confidence_reason(result) == "Middels: 1 utsolgt uke de siste 12 ukene."
    )


def test_a_level_shift_is_named_in_the_reason_and_has_no_warning_text_yet():
    """FR-17, FR-17b: «Middels: nytt nivå de siste 12 ukene.»; the warning text is Should."""
    result = forecast(series(104, spikes={102: 50, 103: 52, 104: 51}))

    assert result.warnings == (trust.LEVEL_SHIFT,)
    assert words.warning_texts(result, *LATEST) == ()
    assert words.confidence_reason(result) == "Middels: nytt nivå de siste 12 ukene."


def test_the_warnings_of_the_recent_period_are_one_phrase_in_r_15_order():
    """FR-19, R-15: stockout weeks, unusual weeks and a level shift read «2 utsolgte uker,
    1 uvanlig uke og nytt nivå de siste 12 ukene»."""
    result = forecast(
        series(104, stockouts={95, 96}, spikes={98: 30, 102: 50, 103: 52, 104: 51})
    )

    assert result.warnings == (
        trust.STOCKOUT_WEEKS,
        trust.UNUSUAL_WEEKS,
        trust.LEVEL_SHIFT,
    )
    assert words.confidence_reason(result) == (
        "Middels: 2 utsolgte uker, 1 uvanlig uke og nytt nivå de siste 12 ukene."
    )


def test_a_short_history_and_few_valid_weeks_each_have_their_reason():
    """FR-19, R-16 (E29 b, g): «Middels: kortere salgshistorikk enn 104 uker.» and
    «Middels: færre enn 100 gyldige uker.»"""
    assert words.confidence_reason(forecast(series(80))) == (
        "Middels: kortere salgshistorikk enn 104 uker."
    )
    assert words.confidence_reason(
        forecast(series(104, stockouts={1, 2, 3, 4, 5}))
    ) == ("Middels: færre enn 100 gyldige uker.")


def test_high_has_the_reason_of_the_catalogue():
    """FR-19, R-16 (E29 c): «Høy: minst 104 uker salgshistorikk, minst 100 gyldige uker og
    ingen varsler.»"""
    result = case_result("E29 c")

    assert result.confidence_label == trust.HOY
    assert words.confidence_reason(result) == (
        "Høy: minst 104 uker salgshistorikk, minst 100 gyldige uker og ingen varsler."
    )
    assert words.warning_texts(result, *LATEST) == ()


def test_a_product_with_a_forecast_has_the_note_of_fr_7_and_no_list_text():
    """FR-7: «Uke 2 og 3 viser samme tall som uke 1 fordi metoden ikke tar hensyn til trend
    eller sesong.» for every product with a forecast, and none for one without."""
    assert words.note_texts(forecast(series(12))) == (FLAT_WEEKS_NOTE,)
    assert words.note_texts(forecast(series(2))) == ()


def test_every_must_warning_has_a_text_for_every_seed_shape():
    """AD-4: each active warning but the level shift (FR-17b) has a text in R-15 order."""
    result = forecast(series(22, stockouts=set(range(3, 23))))

    assert [code for code, _ in texts(result)] == [
        trust.STOCKOUT_WEEKS,
        trust.OLD_DATA,
        trust.INSUFFICIENT_DATA,
    ]


def test_a_level_shift_after_another_condition_is_its_own_sentence():
    """FR-17, FR-19 (E9): «Lav: færre enn 12 gyldige uker. Nytt nivå de siste 12 ukene.»"""
    result = case_result("E9 (included)")

    assert words.confidence_reason(result) == (
        "Lav: færre enn 12 gyldige uker. Nytt nivå de siste 12 ukene."
    )


def test_a_warning_note_or_condition_without_a_text_is_an_error_and_never_left_out():
    """AD-4: a new warning, note or condition must get its wording, so it fails loudly
    until it does (FR-36 and the Should notes come later)."""
    result = forecast(series(104, stockouts={104}))

    with pytest.raises(KeyError):
        words.warning_texts(
            dataclasses.replace(result, warnings=("seasonal_pattern",)), *LATEST
        )
    with pytest.raises(KeyError):
        words.note_texts(dataclasses.replace(result, notes=("overstock",)))
    with pytest.raises(ValueError, match="unknown"):
        words.confidence_reason(
            dataclasses.replace(result, confidence_condition="unknown")
        )
    with pytest.raises(ValueError, match="insufficient-data"):
        words.warning_texts(
            dataclasses.replace(result, warnings=("insufficient_data",)), *LATEST
        )


def test_the_catalogue_has_the_singular_and_marks_the_old_data_phrase_as_a_guard_case():
    """AD-4, FR-8, FR-18: the catalogue and `explanation/` agree on the singular «1 gyldig
    uke» and on the stand-alone old-data phrase, which the catalogue calls a guard case."""
    catalogue = CATALOGUE.read_text(encoding="utf-8")
    one = forecast([Week(5, False)])
    old_data_alone = (
        "«Middels: gamle data, 9 uker siden siste gyldige uke.» (guard case:"
    )

    assert (
        "«Produktet har [1] gyldig uke. Prognose regner ut en prognose når" in catalogue
    )
    assert (
        "Produktet har 1 gyldig uke. Prognose regner ut en prognose når"
        in (texts(one)[0][1])
    )
    assert old_data_alone in catalogue
