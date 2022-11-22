from matching.models import Candidate
from matching.read_in import _read_and_create_objects


def test_candidate_read_in():
    _read_and_create_objects("test_data/candidates.csv", Candidate)
