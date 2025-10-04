from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

from ahse.schemas.mission import MissionConfig
from ahse.schemas.state import PhysiologicalState, SimulationResult
from ahse.models.muscle import update_muscle
from ahse.models.bone import update_bone
from ahse.models.cardio import update_cardio
from ahse.models.immune import update_immune
from ahse.models.cognitive import update_cognitive
from ahse.models.radiation import update_radiation


@dataclass
class InitialState:
    muscle_mass_kg: float = 35.0
    muscle_strength_index: float = 0.75
    bone_density_g_cm2: float = 1.1
    cardio_fitness_vo2max: float = 45.0
    immune_competence_index: float = 0.8
    cognitive_function_index: float = 0.85
    dna_damage_index: float = 0.0


class Simulator:
    def __init__(self, mission: MissionConfig, initial: InitialState | None = None):
        self.mission = mission
        self.initial = initial or InitialState()

    def run(self) -> SimulationResult:
        env = self.mission.environment
        ex = self.mission.exercise
        diet = self.mission.diet
        sleep = self.mission.sleep

        state = PhysiologicalState(
            day=0,
            muscle_mass_kg=self.initial.muscle_mass_kg,
            muscle_strength_index=self.initial.muscle_strength_index,
            bone_density_g_cm2=self.initial.bone_density_g_cm2,
            cardio_fitness_vo2max=self.initial.cardio_fitness_vo2max,
            immune_competence_index=self.initial.immune_competence_index,
            cognitive_function_index=self.initial.cognitive_function_index,
            dna_damage_index=self.initial.dna_damage_index,
        )
        timeline: list[PhysiologicalState] = [state]

        minutes_per_day_exercise = int(round(ex.session_minutes * ex.frequency_per_week / 7))

        for day in range(1, env.duration_days + 1):
            new_mass, new_strength = update_muscle(
                state.muscle_mass_kg,
                state.muscle_strength_index,
                env.microgravity_level,
                minutes_per_day_exercise,
                ex.intensity,
            )
            new_bone = update_bone(state.bone_density_g_cm2, env.microgravity_level, diet.calcium_mg_per_day, diet.vitamin_d_IU_per_day)
            new_vo2 = update_cardio(state.cardio_fitness_vo2max, env.microgravity_level, minutes_per_day_exercise, ex.intensity)
            new_immune = update_immune(state.immune_competence_index, sleep.circadian_stability, sleep.hours_per_day, minutes_per_day_exercise)
            new_cognitive = update_cognitive(state.cognitive_function_index, sleep.hours_per_day, sleep.circadian_stability)
            new_dna = update_radiation(state.dna_damage_index, env.radiation_uSv_per_day)

            state = PhysiologicalState(
                day=day,
                muscle_mass_kg=new_mass,
                muscle_strength_index=new_strength,
                bone_density_g_cm2=new_bone,
                cardio_fitness_vo2max=new_vo2,
                immune_competence_index=new_immune,
                cognitive_function_index=new_cognitive,
                dna_damage_index=new_dna,
            )
            timeline.append(state)

        return SimulationResult(timeline=timeline)
