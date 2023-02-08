from unittest.mock import Mock

import pytest

from fast_stream_22.matching.SEFS.models import SefsPair, SefsCandidate, SefsRole
from fast_stream_22.matching.pair import BasePair


def test_when_pair_created_scoring_method_added_to_parent_class():
    p = SefsPair(Mock(), Mock())
    assert SefsPair._score_skill.__name__ in p.scoring_method_names
    assert BasePair._score_location.__name__ in p.scoring_method_names


class TestScoreSkill:
    @pytest.mark.parametrize(["year_group", "score"], [(1, 0), (2, 36)])
    def test_when_year_all_skills_match_scored_is_correct(
        self, random_candidate_dict, random_role_dict, year_group, score
    ):
        c = SefsCandidate(not_required="Broad Thinking", **random_candidate_dict())
        c.primary_skill = "Developing the GSE community"
        c.secondary_skill = "Building and Applying Knowledge"
        c.year_group = year_group

        r = SefsRole(
            broad_thinking="A",
            building_applying="P",
            communicating="A",
            oversight="A",
            developing="P",
            **random_role_dict()
        )
        p = SefsPair()
        assert p.score == 0
        p._score_skill(c, r)
        assert p.score == score
