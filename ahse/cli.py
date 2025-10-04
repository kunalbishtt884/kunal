from __future__ import annotations
import json
from pathlib import Path
import click
from rich.console import Console
from rich.table import Table

from ahse.utils.io import load_mission_config, save_simulation_json, save_simulation_csv
from ahse.engine.simulator import Simulator
from ahse.recommendation.engine import generate_recommendations

console = Console()


@click.group()
def cli():
    """Astronaut Health Simulation Engine (AHSE) CLI"""


@cli.command()
@click.option("--config", type=click.Path(exists=True, path_type=Path), required=True, help="Mission config JSON path")
@click.option("--out", type=click.Path(path_type=Path), required=True, help="Output directory")
@click.option("--csv/--no-csv", default=True, help="Also save CSV timeline")
@click.option("--json/--no-json", default=True, help="Also save JSON timeline")
def run(config: Path, out: Path, csv: bool, json: bool):
    mission = load_mission_config(config)
    sim = Simulator(mission)
    result = sim.run()

    out.mkdir(parents=True, exist_ok=True)

    if json:
        save_simulation_json(result, out / "timeline.json")
    if csv:
        save_simulation_csv(result, out / "timeline.csv")

    table = Table(title="Final State")
    for key in result.timeline[-1].model_dump().keys():
        table.add_column(key)
    table.add_row(*[str(v) for v in result.timeline[-1].model_dump().values()])
    console.print(table)

    recs = generate_recommendations(result)
    if recs:
        console.print("[bold]Recommendations:[/bold]")
        for r in recs:
            console.print(f"- [{r.category}] {r.message}")
    else:
        console.print("No recommendations; parameters are within acceptable ranges.")


if __name__ == "__main__":
    cli()
