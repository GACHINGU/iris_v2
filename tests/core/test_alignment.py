# tests/core/test_alignment.py

from datetime import date
import pytest
from core.alignment import rate_on, build_aligned_days
from data_access.contracts import CBRDecision, KCBDailyPrice, AlignedDay

DECISIONS = [
    CBRDecision(decision_date=date(2020, 1, 10), rate=8.0),
    CBRDecision(decision_date=date(2020, 3, 1), rate=7.5),
    CBRDecision(decision_date=date(2020, 5, 20), rate=7.0),
]


def make_price(day, close) -> KCBDailyPrice:
    """
    Is a helper function that helps us create KCB ticker data form instantly.
    It fills the open, high, low, close with the same number because the tests
    only care about the close.
    Instead of retyping six fields in every test.
    """
    form = KCBDailyPrice(
        trade_date=day,
        open_price=close,
        high_price=close,
        low_price=close,
        close_price=close,
        volume=100,
    )
    return form


def test_rate_on_returns_none_before_first_decision() -> None:
    """
    We intentionally put a date before the CBR decisions started being recorded to
    see if the function rate_on returns None, instead of failing silently.
    """
    assert rate_on(date(2020, 1, 5), DECISIONS) is None


def test_rate_on_counts_a_decision_on_its_own_day() -> None:
    """
    Checking whether rate_on correctly assigns the rate to its own true day.
    """
    assert rate_on(date(2020, 3, 1), DECISIONS) == 7.5


def test_rate_on_returns_most_recent_decision_between_notices() -> None:
    """
    Checking whether rate_on correctly assigns a day with the most recent decision,
    in between notices.
    """
    assert rate_on(date(2020, 3, 15), DECISIONS) == 7.5


def test_build_aligned_days_attaches_the_rate_in_effect_to_each_day() -> None:
    """
    Testing whether the build_aligned_days function peggs the right decision rate,
    on the right date and the right price. These protects against data lose when a
    shuffle accidentally occurs.
    """
    prices = [make_price(date(2020, 1, 5), 10.0), make_price(date(2020, 3, 15), 11.0)]

    results = build_aligned_days(prices, DECISIONS)

    assert results == [
        AlignedDay(trade_date=date(2020, 1, 5), close_price=10.0, cbr_rate=None),
        AlignedDay(trade_date=date(2020, 3, 15), close_price=11.0, cbr_rate=7.5),
    ]


def test_build_aligned_days_rejects_a_newest_first_list() -> None:
    """
    We intentionally reverse the DECISIONS such that the newest dates start first.
    These is to test whether the alarm switch we put in the build_aligned_days
    function rejects these order.
    """
    newest_first = list(reversed(DECISIONS))
    prices = [make_price(date(2020, 3, 15), 11.0)]

    with pytest.raises(ValueError):
        build_aligned_days(prices=prices, decisions_oldest_first=newest_first)
