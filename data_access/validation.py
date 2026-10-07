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


def is_chronologically_ordered(dates: list, increasing: bool = True) -> bool:
    """
    These function checks the dates chronological order, if the increasing switch is set to True,
    then only checks the if condition under the if increasing == True, if the increasing switch is
    set to False, python jumps the first if condition directly to the else condition and checks
    whether date is chronologically ordered the way it will be needed. Returns a hard coded True
    if no flag is detected, and False if date is not ordered as expected. increasing: bool = True
    is the switch.
    """
    for i in range(1, len(dates)):
        if increasing:
            if dates[i] < dates[i - 1]:  # the decreasing instead of increasing flag
                return False

        else:
            if dates[i] > dates[i - 1]:  # the increasing instead of decreasing flag
                return False
    return True
