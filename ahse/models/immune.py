from __future__ import annotations
from pydantic import BaseModel


class ImmuneParams(BaseModel):
    decline_per_day_stress: float = 0.002
    sleep_stability_buffer: float = 0.001
    exercise_benefit: float = 0.0008


def update_immune(immune_index: float, circadian_stability: float, sleep_hours: float, exercise_minutes: int) -> float:
    stress_decline = ImmuneParams().decline_per_day_stress * (1.0 - circadian_stability)
    sleep_bonus = ImmuneParams().sleep_stability_buffer * max(0.0, (sleep_hours - 7.0) / 2.0)
    exercise_bonus = ImmuneParams().exercise_benefit * min(1.0, exercise_minutes / 60.0)
    new_index = max(0.0, min(1.0, immune_index - stress_decline + sleep_bonus + exercise_bonus))
    return new_index
