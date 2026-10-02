# tests/data_access/test_parsers.py

from data_access.parsers import parse_cbr_row
from data_access.parsers import parse_kcb_row
from data_access.contracts import CBRDecision
from data_access.contracts import KCBDailyPrice
from datetime import date


def test_parse_cbr_row_reads_day_before_month() -> None:
    """
    Tests whether the conversion of string date to actual date happens and
    happens in the right order date(year, month, day).
    Also checks whether the rate string is rightfully converted to a float.
    """
    row = {"Date": "11/08/2026", "Rate": "8.75"}
    expected = CBRDecision(decision_date=date(2026, 8, 11), rate=8.75)
    assert parse_cbr_row(row) == expected


def test_parse_kcb_row_reads_year_first() -> None:
    """
    Tests whether the conversion of the string date to actual data happens and
    happens un the right order date(Year, month, day).
    Also checks whether the conversion of numbers to their required types happens.
    """
    row = {
        "date": "1996-06-26",
        "open": "7.21",
        "high": 7.21,
        "low": 7.21,
        "close": 7.21,
        "volume": 171517,
    }

    expected = KCBDailyPrice(
        trade_date=date(1996, 6, 26),
        open_price=7.21,
        high_price=7.21,
        low_price=7.21,
        close_price=7.21,
        volume=171517,
    )

    assert parse_kcb_row(row) == expected
