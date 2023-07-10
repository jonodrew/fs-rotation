from unittest.mock import MagicMock

import pytest

from fast_stream_22.specialism.models import (
    Candidate,
    Role,
    Nationality,
    NationalityRequirement,
)
from fast_stream_22.specialism.pair import Pair


@pytest.fixture
def pair_with_mocks():
    role = MagicMock(Role)
    role.priority_role = False
    return Pair(MagicMock(spec=Candidate, create=True), role)


class TestPair:
    def test_location_score(self, pair_with_mocks):
        pair = pair_with_mocks
        pair.candidate.can_relocate = True
        pair.candidate.first_preference_location = "Toontown"
        pair.role.locations = "Toontown"
        pair.candidate.has_relocated = False
        pair._score_location()
        assert not pair.disqualified
        assert pair._score == pair.scoring_weights["first_location"]

    def test_location_when_any(self, pair_with_mocks):
        pair = pair_with_mocks
        pair.candidate.can_relocate = True
        pair.candidate.first_preference_location = "Any"
        pair.candidate.second_preference_location = "Any"
        pair.role.locations = "Toontown"
        pair.candidate.has_relocated = False
        pair._score_location()
        assert pair._score == pair.scoring_weights["first_location"]

    def test_nationality_check(self, pair_with_mocks):
        pair = pair_with_mocks
        pair.candidate.british_national = Nationality["DUAL_NATIONAL"]
        pair.role.nationality_requirement = NationalityRequirement["BRITISH_NATIONAL"]
        pair._check_nationality()
        assert pair.disqualified
