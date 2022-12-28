import csv
from functools import partial

import click
from fast_stream_22.matching.match import Process, Bid
from fast_stream_22.matching.read_in import read_candidates, read_roles
import time


@click.command
@click.option(
    "--candidates", help="Path to candidates file", default="./candidates.csv", type=str
)
@click.option("--roles", help="Path to roles file", default="./roles.csv", type=str)
@click.option(
    "--bids", help="Path to file containing bids", default="./bids.csv", type=str
)
def process_matches(bids: str, roles: str, candidates: str):
    start = time.time()
    cohort_pairings = conduct_matching(bids, roles, candidates)
    for cohort in cohort_pairings.values():
        for pair in cohort:
            print(pair[0], pair[1])
    end = time.time()
    print(f"Task completed in {(end-start)*1000} milliseconds")


def conduct_matching(
    bid_file: str = "./bids.csv",
    role_file: str = "./roles.csv",
    candidate_file: str = "./roles.csv",
):
    dept_bids = []
    with open(bid_file) as bids_file:
        bids_reader = csv.reader(bids_file)
        for row in bids_reader:
            partial_bid = partial(Bid, department=row[0])
            for cohort, value in enumerate(row[1:]):
                dept_bids.extend([partial_bid(cohort=cohort + 1, number=int(value))])
    process_obj = Process(
        read_candidates(candidate_file), read_roles(role_file), dept_bids
    )
    process_obj.compute()
    return process_obj.pairings
