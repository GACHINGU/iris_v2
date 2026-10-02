# data_access/parsers.py

from datetime import datetime
from data_access.contracts import CBRDecision
from data_access.contracts import KCBDailyPrice
import csv


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


def load_cbr_decisions(path: str) -> list[CBRDecision]:
    """
    Opens up the cbr.csv and make sure its safe from source to form.
    Returns a lists of CBRDecisions forms.
    """
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        decisions = [parse_cbr_row(row) for row in reader]
        return decisions


def load_kcb_prices(path: str) -> list[KCBDailyPrice]:
    """
    Opens up the kcb.csv and makes sure its safe from source to form.
    Returns a list of KCBDailyPrice forms.
    """
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        prices = [parse_kcb_row(row) for row in reader]

        return prices
