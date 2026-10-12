# core/alignment.py
from datetime import date

from data_access.contracts import CBRDecision, KCBDailyPrice, AlignedDay
from data_access.validation import is_chronologically_ordered


def rate_on(query: date, decisions_oldest_first: list[CBRDecision]) -> float | None:
    """
    These function's core task is to give each KCB price ticker a cbr rate.
    It checks whether the decision date is larger or smaller than the query
    date (what represents KCB date), and if smaller or equal to query,
    assigns it a rate. If date is way to small than the first decision it
    simply assigns None, nothing gets overwritten.
    """
    rate_on_effect = None
    for decision in decisions_oldest_first:
        if decision.decision_date <= query:
            rate_on_effect = decision.rate

    return rate_on_effect


def build_aligned_days(
    prices: list[KCBDailyPrice], decisions_oldest_first: list[CBRDecision]
) -> list[AlignedDay]:
    """
    The function aligns days, prices with their rates, through a strict form,
    To prevent scrumbled data incase of a shuffle. True data is maintained.
    date pegged with its true price and pegged with its True rate.
    """
    decision_dates = [day.decision_date for day in decisions_oldest_first]
    if not is_chronologically_ordered(decision_dates, increasing=True):
        raise ValueError("CBR decisions must be sorted oldest to newest")

    form = [
        AlignedDay(
            trade_date=price.trade_date,
            close_price=price.close_price,
            cbr_rate=rate_on(
                query=price.trade_date, decisions_oldest_first=decisions_oldest_first
            ),
        )
        for price in prices
    ]

    return form
