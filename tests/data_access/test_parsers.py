# tests/data_access/test_parsers.py

from data_access.parsers import parse_cbr_row
from data_access.contracts import CBRDecision
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
