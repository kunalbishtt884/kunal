from __future__ import annotations
from pydantic import BaseModel


class RadiationParams(BaseModel):
    damage_per_uSv: float = 1e-6
    repair_fraction_per_day: float = 0.02


def update_radiation(dna_damage_index: float, daily_dose_uSv: float) -> float:
    new_damage = dna_damage_index * (1.0 - RadiationParams().repair_fraction_per_day) + daily_dose_uSv * RadiationParams().damage_per_uSv
    return max(0.0, new_damage)
