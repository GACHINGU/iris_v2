# data_access/parsers.py

from datetime import datetime
from data_access.contracts import CBRDecision
from data_access.contracts import KCBDailyPrice


def parse_cbr_row(row: dict) -> CBRDecision:
    """
    Translates one raw CBR csv row into a filled-in CBRDecision form.
    """
    parsed_date = datetime.strptime(
        row["Date"], "%d/%m/%Y"
    ).date()  # change the string date into actual date, date() makes the date lean, with no time
    parsed_rate = float(row["Rate"])  # convert the string rates to float
    form = CBRDecision(decision_date=parsed_date, rate=parsed_rate)
    return form


def parse_kcb_row(row: dict) -> KCBDailyPrice:
    """
    Translates one raw KCB csv row into a filled-in KCBDaily form.
    """
    parsed_date = datetime.strptime(row["date"], "%Y-%m-%d").date()

    form = KCBDailyPrice(
        trade_date=parsed_date,
        open_price=float(row["open"]),
        high_price=float(row["high"]),
        low_price=float(row["low"]),
        close_price=float(row["close"]),
        volume=int(row["volume"]),
    )

    return form
