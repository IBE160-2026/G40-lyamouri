"""The overview of a company's products (R-12; FR-24; AD-2, UX-DR33, UX-DR35).

`build_overview` groups and orders the results of the products, gives the four week
figures, the review sequence and the previous and next product of each product. It works
on product numbers, which are text and sort as text, and on the results from
`forecast_product`; the caller joins the numbers with the results. It keeps full float
precision and sorts by the unrounded weeks of cover, so nothing is rounded before the
order is set (AD-3), and it gives numbers only and no text (AD-4). Only the standard
library is imported (AD-1).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class WeekFigures:
    """The four figures of «Denne uken» (UX-DR33): the products with order-soon status, the
    sum of the suggested order quantities, the products without a forecast and the
    products with at least one active warning."""

    order_soon: int
    units_suggested: int
    without_forecast: int
    with_warning: int


@dataclass(frozen=True)
class Neighbours:
    """The previous and next product in overview order, across all groups (UX-DR35), or
    None at the first and the last product."""

    previous: str | None
    next: str | None


@dataclass(frozen=True)
class Overview:
    """The overview of a company, as product numbers.

    `order_soon`, `without_forecast` and `others` are the three groups of R-12 in that
    order, and `order` is the three together. `review_sequence` is the order-soon
    products and then those without a forecast. `neighbours` has an entry for each product.
    """

    order_soon: tuple[str, ...]
    without_forecast: tuple[str, ...]
    others: tuple[str, ...]
    order: tuple[str, ...]
    review_sequence: tuple[str, ...]
    figures: WeekFigures
    neighbours: dict[str, Neighbours]


def build_overview(results, adjustments):
    """Group and order the products of a company by R-12.

    `results` maps each product number to its `ProductResult`. `adjustments` is empty
    until FR-29 is built, and a non-empty one is refused, so that an adjustment is never
    ignored silently. The order-soon products come first, by weeks of cover and then by
    product number (E24); then the products without a forecast, and then the rest, each
    by product number.
    """
    if adjustments:
        raise ValueError("adjustments come with FR-29 and are not built yet")

    order_soon = sorted(
        (number for number, result in results.items() if result.order_soon),
        key=lambda number: (results[number].weeks_of_cover, number),
    )
    without_forecast = sorted(
        number for number, result in results.items() if result.base_forecast is None
    )
    grouped = {*order_soon, *without_forecast}
    others = sorted(number for number in results if number not in grouped)

    order = (*order_soon, *without_forecast, *others)
    neighbours = {
        number: Neighbours(
            previous=order[index - 1] if index > 0 else None,
            next=order[index + 1] if index + 1 < len(order) else None,
        )
        for index, number in enumerate(order)
    }
    figures = WeekFigures(
        order_soon=len(order_soon),
        units_suggested=sum(
            result.suggested_order_quantity or 0 for result in results.values()
        ),
        without_forecast=len(without_forecast),
        with_warning=sum(1 for result in results.values() if result.warnings),
    )
    return Overview(
        order_soon=tuple(order_soon),
        without_forecast=tuple(without_forecast),
        others=tuple(others),
        order=order,
        review_sequence=(*order_soon, *without_forecast),
        figures=figures,
        neighbours=neighbours,
    )
