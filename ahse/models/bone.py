from __future__ import annotations
from pydantic import BaseModel


class BoneParams(BaseModel):
    loss_rate_per_day_microgravity: float = 0.001  # ~0.1%/day
    calcium_intake_effect_threshold_mg: int = 1000
    vitamin_d_effect_threshold_IU: int = 800


def update_bone(bone_density_g_cm2: float, microgravity: float, calcium_mg: float, vitamin_d_IU: float) -> float:
    loss = bone_density_g_cm2 * (microgravity * BoneParams().loss_rate_per_day_microgravity)
    intake_factor = 0.0
    if calcium_mg >= BoneParams().calcium_intake_effect_threshold_mg:
        intake_factor += 0.0003
    if vitamin_d_IU >= BoneParams().vitamin_d_effect_threshold_IU:
        intake_factor += 0.0002
    new_density = max(0.0, bone_density_g_cm2 - loss + bone_density_g_cm2 * intake_factor)
    return new_density
