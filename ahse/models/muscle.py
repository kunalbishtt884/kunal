from __future__ import annotations
from pydantic import BaseModel


class MuscleParams(BaseModel):
    atrophy_rate_per_day_microgravity: float = 0.003  # ~0.3% mass/day
    recovery_rate_per_day_with_exercise: float = 0.002


def update_muscle(muscle_mass_kg: float, strength_index: float, microgravity: float, exercise_minutes: int, intensity: float) -> tuple[float, float]:
    atrophy = muscle_mass_kg * (microgravity * MuscleParams().atrophy_rate_per_day_microgravity)
    recovery = muscle_mass_kg * (intensity * exercise_minutes / 60.0) * MuscleParams().recovery_rate_per_day_with_exercise
    new_mass = max(0.0, muscle_mass_kg - atrophy + recovery)

    strength_decay = 0.002 * microgravity
    strength_gain = 0.003 * intensity * (exercise_minutes / 60.0)
    new_strength = max(0.0, min(1.0, strength_index - strength_decay + strength_gain))
    return new_mass, new_strength
