from __future__ import annotations
from pydantic import BaseModel


class CardioParams(BaseModel):
    vo2_decline_per_day_microgravity: float = 0.002
    vo2_gain_per_hour_exercise: float = 0.004


def update_cardio(vo2max: float, microgravity: float, exercise_minutes: int, intensity: float) -> float:
    decline = vo2max * (microgravity * CardioParams().vo2_decline_per_day_microgravity)
    gain = vo2max * (intensity * (exercise_minutes / 60.0) * CardioParams().vo2_gain_per_hour_exercise)
    return max(0.0, vo2max - decline + gain)
