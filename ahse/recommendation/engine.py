from __future__ import annotations
from dataclasses import dataclass
from typing import List

from ahse.schemas.state import SimulationResult


@dataclass
class Recommendation:
    category: str
    message: str


def generate_recommendations(result: SimulationResult) -> List[Recommendation]:
    recs: List[Recommendation] = []
    if len(result.timeline) < 2:
        return recs

    final = result.timeline[-1]
    start = result.timeline[0]

    if final.muscle_mass_kg < 0.95 * start.muscle_mass_kg:
        recs.append(Recommendation(
            category="exercise",
            message="Increase resistance exercise intensity by 10-15% and add 1 session/week."
        ))

    if final.bone_density_g_cm2 < 0.98 * start.bone_density_g_cm2:
        recs.append(Recommendation(
            category="nutrition",
            message="Ensure ≥1200 mg calcium and ≥1000 IU vitamin D per day."
        ))

    if final.cardio_fitness_vo2max < 0.95 * start.cardio_fitness_vo2max:
        recs.append(Recommendation(
            category="exercise",
            message="Add 2x/week HIIT sessions (20 min) to improve VO2max."
        ))

    if final.immune_competence_index < 0.8:
        recs.append(Recommendation(
            category="sleep",
            message="Stabilize circadian schedule; target 8 hours/night for immune support."
        ))

    if final.dna_damage_index > 0.5:
        recs.append(Recommendation(
            category="radiation",
            message="Increase shielding or adjust mission EVA schedule to reduce dose."
        ))

    if final.cognitive_function_index < 0.8:
        recs.append(Recommendation(
            category="behavioral",
            message="Introduce cognitive training and optimize light exposure timing."
        ))

    return recs
