from unittest.mock import Mock

import pytest

from fast_stream_22.matching.SEFS.models import SefsPair, SefsCandidate, SefsRole
from fast_stream_22.matching.pair import BasePair


def test_when_pair_created_scoring_method_added_to_parent_class():
    p = SefsPair(Mock(), Mock())
    assert SefsPair._score_skill.__name__ in p.scoring_method_names
    assert BasePair._score_location.__name__ in p.scoring_method_names


@pytest.fixture
def sefs_candidate(random_candidate_dict):
    c = SefsCandidate(not_required="Broad Thinking", **random_candidate_dict())
    c.primary_skill = "Developing the GSE community"
    c.secondary_skill = "Building and Applying Knowledge"
    return c


@pytest.fixture
def sefs_role(random_role_dict):
    return SefsRole(
        broad_thinking="A",
        building_applying="P",
        communicating="A",
        oversight="A",
        developing="P",
        **random_role_dict()
    )


class TestScoreSkill:
    @pytest.mark.parametrize(["year_group", "score"], [(1, 0), (2, 36)])
    def test_when_year_all_skills_match_scored_is_correct(
        self, sefs_candidate, sefs_role, year_group, score
    ):
        c = sefs_candidate
        c.primary_skill = "Developing the GSE community"
        c.secondary_skill = "Building and Applying Knowledge"
        c.year_group = year_group

        r = sefs_role
        p = SefsPair()
        assert p.score == 0
        p._score_skill(c, r)
        assert p.score == score
