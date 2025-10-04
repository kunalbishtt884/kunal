from __future__ import annotations
from pydantic import BaseModel, Field, confloat


class PhysiologicalState(BaseModel):
    day: int = 0
    muscle_mass_kg: confloat(gt=0)
    muscle_strength_index: confloat(ge=0, le=1)
    bone_density_g_cm2: confloat(gt=0)
    cardio_fitness_vo2max: confloat(gt=0)
    immune_competence_index: confloat(ge=0, le=1)
    cognitive_function_index: confloat(ge=0, le=1)
    dna_damage_index: confloat(ge=0) = Field(
        0.0, description="Cumulative relative DNA damage (arbitrary units)"
    )


class SimulationResult(BaseModel):
    timeline: list[PhysiologicalState]
