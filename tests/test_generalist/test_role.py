import csv
from fast_stream_22.matching.generalist.models import GeneralistRole


def test_instantiation_from_csv_data():
    with open("tests/test_generalist/test_roles.csv") as test_file:
        r = csv.DictReader(test_file)
        rows = [GeneralistRole(**row) for row in r]
    assert rows
