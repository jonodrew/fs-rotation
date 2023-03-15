import click

from fast_stream_22.matching.match import conduct_matching
import time


@click.command
@click.option(
    "--iterations", help="The number of iterations to go through", default=10, type=int
)
@click.option("--specialism", help="The scheme specialism", default=None, type=str)
@click.option("--senior_first", help="Match seniors first", default=True, type=bool)
@click.option(
    "--candidates", help="Path to candidates file", default="./candidates.csv", type=str
)
@click.option("--roles", help="Path to roles file", default="./roles.csv", type=str)
@click.option(
    "--bids", help="Path to file containing bids", default="./bids.csv", type=str
)
def process_matches(
    bids: str,
    roles: str,
    candidates: str,
    senior_first: bool,
    specialism: str,
    iterations: int,
):
    start = time.time()
    cohort_pairings = conduct_matching(
        bids, roles, candidates, senior_first, specialism, iterations
    )
    end = time.time()
    for iteration, outcome in cohort_pairings.items():
        for cohort_name, cohort in outcome.outcomes.items():
            for pair in cohort:
                click.echo(f"{iteration},{cohort_name.name},{','.join(map(str, pair))}")
    best_iteration_by_score = max(
        cohort_pairings.values(), key=lambda outcome: outcome.total_score
    )
    best_iteration_by_success_bound = max(
        cohort_pairings.values(), key=lambda outcome: outcome.success_count
    )
    click.echo(f"Task completed in {(end-start)} seconds")
    click.echo(f"Best iteration by score: {best_iteration_by_score.iteration}")
    click.echo(
        "Best iteration by departments scoring above criteria"
        f" ({best_iteration_by_success_bound.success_count}):"
        f" {best_iteration_by_success_bound.iteration}"
    )
