"""The template filters for domain numbers (AD-3).

They only call `forecasting/display.py`, so a template never rounds or formats a number
itself.
"""

from django import template

from forecasting import display

register = template.Library()

register.filter("one_decimal", display.one_decimal)
register.filter("two_decimals", display.two_decimals)
register.filter("whole_number", display.whole_number)
register.filter("percent", display.percent)
register.filter("weeks_of_cover", display.weeks_of_cover)
register.filter("suggested_quantity", display.suggested_quantity)
