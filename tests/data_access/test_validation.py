# tests/data_access/test_validation

from datetime import date
from data_access.contracts import CBRDecision
from data_access.validation import deduplicate_cbr_decisions
from data_access.validation import is_chronologically_ordered


def test_deduplicate_cbr_decisions_drops_repeated_dates() -> None:
    """
    Test whether the deduplicate function drops repeated rows and
    preserve the order of the data.
    """
    decisions = [
        CBRDecision(decision_date=date(2019, 5, 27), rate=9.0),
        CBRDecision(decision_date=date(2019, 5, 27), rate=9.0),
        CBRDecision(decision_date=date(2020, 5, 27), rate=7.0),
    ]

    result = deduplicate_cbr_decisions(decisions=decisions)

    assert len(result) == 2
    assert result[0].decision_date == date(2019, 5, 27)
    assert result[1].decision_date == date(2020, 5, 27)


def test_is_chronologically_ordered_detects_a_backward_step() -> None:
    """
    Test whether the function has the ability to flag a backward step,
    when increasing is expected. Achieved by creating a fake broken data.
    """

    broken_dates = [date(2020, 1, 1), date(2020, 1, 3), date(202, 1, 2)]
    assert is_chronologically_ordered(broken_dates, increasing=True) is False


def test_is_chronologically_ordered_passes_clean_increasing_dates() -> None:
    """
    Test whether the function actually acknowledges and accepts increasing
    clean dates as True when the switch is set to True.
    """
    clean_dates_toy = [date(2020, 1, 1), date(2020, 1, 2), date(2020, 1, 3)]
    assert is_chronologically_ordered(clean_dates_toy, increasing=True)
