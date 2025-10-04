from __future__ import annotations

from ahse.utils.io import load_mission_config
from ahse.engine.simulator import Simulator


def test_simulation_runs():
    mission = load_mission_config("examples/sample_mission.json")
    sim = Simulator(mission)
    result = sim.run()
    assert len(result.timeline) == mission.environment.duration_days + 1


def test_recommendations_thresholds():
    mission = load_mission_config("examples/sample_mission.json")
    sim = Simulator(mission)
    result = sim.run()
    # End state should be a valid state with indices bounded
    final = result.timeline[-1]
    assert 0.0 <= final.muscle_strength_index <= 1.0
    assert 0.0 <= final.immune_competence_index <= 1.0
    assert 0.0 <= final.cognitive_function_index <= 1.0
