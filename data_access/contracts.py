# data_access/contracts.py
from dataclasses import dataclass
from datetime import date


@dataclass(
    frozen=True
)  # the @dataclasss builds the form, and the frozen=True blocks future changes
class CBRDecision:
    decision_date: date  # represents when the MPC met, the date is a type hint
    rate: float  # represents the CBR that was agreed by the MPC, float is a type hint


@dataclass(frozen=True)
class KCBDailyPrice:
    trade_date: date  # data of the ticker data, date is the type hint
    open_price: float  # on that date what was the opening price, float type hint
    high_price: float  # The highest price recorded on that day, float type hint
    low_price: float  # the lowest price recorded on that day, float type hint
    close_price: float  # the closing price on that date, float type hint
    volume: int  # number of shares being traded that day, is expected to be integer because you cant trade a half a share
