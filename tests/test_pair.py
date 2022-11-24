from unittest.mock import MagicMock

import pytest

from matching.models import Pair, Candidate, Role


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
        pair.role.location = "Toontown"
        pair._score_location()
        assert not pair.disqualified
        assert pair._score == pair.scoring_weights["first_location"]
