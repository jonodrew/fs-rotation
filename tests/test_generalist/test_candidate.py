import csv

import pytest

from fast_stream_22.specialism.generalist import GeneralistCandidate


@pytest.fixture
def generalist_candidate_dict(random_candidate_dict) -> dict:
    return {
        **random_candidate_dict(),
        "primary_anchor_seeking": "Primary Anchor",
        "secondary_anchor_seeking": "Secondary Anchor",
        "dept_pref_1": "0",
        "dept_pref_2": "1",
        "dept_pref_3": "2",
        "dept_pref_4": "3",
        "dept_pref_5": "4",
        "travel_requirements": "I can travel nationally",
    }


@pytest.fixture
def generalist_candidate(generalist_candidate_dict):
    return GeneralistCandidate(**generalist_candidate_dict)


def test_instantiation_from_csv_data():
    with open("tests/test_generalist/test_candidates.csv") as test_file:
        r = csv.DictReader(test_file)
        candidates = [GeneralistCandidate(**row) for row in r]
    assert candidates
