# data_access/contracts.py
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)  # the decorator function that blocks changes afterwards
class CBRDecision:
    decision_date: date  # expected data through is date
    rate: float  # expected data through is float, decimal like


@dataclass(frozen=True)
class KCBDailyPrice:
    trade_date: date
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
