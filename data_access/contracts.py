# data_access/contracts.py
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class CBRDecision:
    decision_date: date
    rate: float
