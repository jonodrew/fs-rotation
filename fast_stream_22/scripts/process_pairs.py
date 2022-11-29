import click
from fast_stream_22.matching.match import Matching
from fast_stream_22.matching.read_in import read_candidates, read_roles
from numpy import savetxt


@click.command
@click.option(
    "--candidates", help="Path to candidates file", default="./candidates.csv", type=str
)
@click.option("--roles", help="Path to roles file", default="./roles.csv", type=str)
def process_matches(roles: str, candidates: str):
    match = Matching(read_candidates(candidates), read_roles(roles))
    savetxt("grid.csv", match.score_grid, fmt="%s", delimiter=",")
    matches = match.report_pairs()
    for pair in matches:
        print(f"{pair[0]},{pair[1]}")
