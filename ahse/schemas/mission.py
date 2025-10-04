from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel, Field, PositiveInt, confloat, conint


class ExerciseRegimen(BaseModel):
    frequency_per_week: conint(ge=0, le=14) = Field(..., description="Workout sessions per week")
    session_minutes: PositiveInt = Field(..., description="Minutes per session")
    intensity: confloat(ge=0.0, le=1.0) = Field(..., description="0-1 relative intensity scale")


class DietProfile(BaseModel):
    calories_per_day: PositiveInt
    protein_g_per_day: confloat(gt=0)
    calcium_mg_per_day: confloat(gt=0)
    vitamin_d_IU_per_day: confloat(gt=0)
    sodium_mg_per_day: confloat(gt=0)


class SleepSchedule(BaseModel):
    hours_per_day: confloat(ge=0, le=24) = 7.5
    circadian_stability: confloat(ge=0.0, le=1.0) = Field(
        0.7, description="Regularity/consistency of sleep timing (0-1)"
    )


class MissionEnvironment(BaseModel):
    duration_days: PositiveInt
    microgravity_level: confloat(ge=0.0, le=1.0) = Field(
        1.0, description="1=full microgravity, 0=Earth gravity"
    )
    radiation_uSv_per_day: confloat(ge=0.0) = Field(..., description="Daily dose rate")


class MissionConfig(BaseModel):
    environment: MissionEnvironment
    exercise: ExerciseRegimen
    diet: DietProfile
    sleep: SleepSchedule
    astronaut_profile: Optional[str] = Field(
        None, description="Identifier for baseline astronaut profile"
    )
