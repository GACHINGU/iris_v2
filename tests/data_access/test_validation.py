# tests/data_access/test_validation

from datetime import date
from data_access.contracts import CBRDecision
from data_access.validation import deduplicate_cbr_decisions


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
