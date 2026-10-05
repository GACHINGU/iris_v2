# data_access/validation.py


def deduplicate_cbr_decisions(decisions: list) -> list:
    """
    These function deals with the duplicate CBR decision rows, where a MPC
    decision was recorded more than once on the same date. These is achieved
    by the help of a bodyguard named set() that makes sure no row appears more
    than once in the cleaned list.

    The end result is a clean list. All with unidue CBR decisions.
    """
    seen = set()
    unique_decisions = []

    for decision in decisions:
        if decision.decision_date not in seen:
            unique_decisions.append(decision)
            seen.add(decision.decision_date)

    return unique_decisions
