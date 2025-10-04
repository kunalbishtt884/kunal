from __future__ import annotations
from pydantic import BaseModel


class CognitiveParams(BaseModel):
    decline_per_day_sleep_debt: float = 0.0015
    improvement_per_day_sleep_surplus: float = 0.0008


def update_cognitive(cognitive_index: float, sleep_hours: float, circadian_stability: float) -> float:
    sleep_debt = max(0.0, 7.5 - sleep_hours)
    sleep_surplus = max(0.0, sleep_hours - 7.5)
    decline = CognitiveParams().decline_per_day_sleep_debt * sleep_debt * (1.1 - circadian_stability)
    improvement = CognitiveParams().improvement_per_day_sleep_surplus * sleep_surplus * circadian_stability
    new_index = max(0.0, min(1.0, cognitive_index - decline + improvement))
    return new_index
