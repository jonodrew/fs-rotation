import click
from click import echo
from fast_stream_22.matching.match import Matching
from fast_stream_22.matching.read_in import read_candidates, read_roles


@click.command
def process_matches():
    matches = Matching(read_candidates(), read_roles()).report_pairs()
    echo(matches)
