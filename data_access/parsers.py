# data_access/parsers.py

from datetime import datetime
from data_access.contracts import CBRDecision


def parse_cbr_row(row: dict) -> CBRDecision:
    """
    This function takes a row of data each, handed to it by python.
    Its main function is to give the right labels to each key of the dictionary
    And also lock the data so its unchangeable.
    All returned as a form, instead of a tuple
    """
    parsed_date = datetime.strptime(
        row["Date"], "%d/%m/%Y"
    ).date()  # change the string date into actual date, date() makes the date lean, with no time
    parsed_rate = float(row["Rate"])  # convert the string rates to float
    form = CBRDecision(decision_date=parsed_date, rate=parsed_rate)
    return form
