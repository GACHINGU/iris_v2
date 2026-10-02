# tests/data_access/test_parsers.py

from data_access.parsers import parse_cbr_row
from data_access.parsers import parse_kcb_row
from data_access.contracts import CBRDecision
from data_access.contracts import KCBDailyPrice
from data_access.parsers import load_kcb_prices, load_cbr_decisions
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


def test_load_cbr_decisions_reads_all_rows_from_file(tmp_path) -> None:
    """
    Test whether the function load_cbr_decision reads every row from
    the csv file and gives back a list of CBRDecision forms.
    """
    cbr_file = tmp_path / "sample_cbr.csv"

    cbr_file.write_text(
        '"Date","Rate"\n"11/08/2026","8.75"\n"09/06/2026","8.75"\n"10/02/2026","9.00"\n'
    )

    decisions = load_cbr_decisions(str(cbr_file))

    assert len(decisions) == 3
    assert decisions[0] == CBRDecision(decision_date=date(2026, 8, 11), rate=8.75)


def test_load_kcb_prices_reads_all_rows_from_file(tmp_path) -> None:
    """
    Tests whether the function load_kcb_prices reads every row from
    the csvfile and gives back a list of KCBDailyPrice forms.
    """
    kcb_file = tmp_path / "sample_ksb.csv"

    kcb_file.write_text(
        "date,open,high,low,close,volume\n"
        "1997-06-26,7.21,7.21,7.21,7.21,171517\n"
        "1997-07-07,7.21,7.21,7.21,7.21,188297\n"
    )

    prices = load_kcb_prices(str(kcb_file))

    assert len(prices) == 2
    assert prices[0].trade_date == date(1997, 6, 26)
