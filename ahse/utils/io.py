from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable

from pydantic import BaseModel

from ahse.schemas.mission import MissionConfig
from ahse.schemas.state import SimulationResult


def load_mission_config(path: str | Path) -> MissionConfig:
    data = json.loads(Path(path).read_text())
    return MissionConfig.model_validate(data)


def save_simulation_json(result: SimulationResult, out_path: str | Path) -> None:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [s.model_dump() for s in result.timeline]
    path.write_text(json.dumps(data, indent=2))


def save_simulation_csv(result: SimulationResult, out_path: str | Path) -> None:
    import csv

    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(result.timeline[0].model_dump().keys())
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in result.timeline:
            writer.writerow(s.model_dump())
