import pytest

from fast_stream_22.matching.generalist.models import GeneralistCandidate


@pytest.fixture
def generalist_candidate(random_candidate_dict):
    return GeneralistCandidate(
        "Primary Anchor",
        "Secondary Anchor",
        "One",
        "Two",
        "Three",
        "Four",
        "Five",
        **random_candidate_dict()
    )


def test_year_group_ending_m_sets_secondment_flag(generalist_candidate):
    assert not generalist_candidate.secondment
    generalist_candidate.year_group = "6m"
    assert generalist_candidate.secondment
    assert generalist_candidate.year_group == 2
