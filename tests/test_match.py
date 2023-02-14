from unittest.mock import patch

from munkres import DISALLOWED

from fast_stream_22.matching.match import Matching
from fast_stream_22.matching.models import Candidate, Role
from fast_stream_22.matching.pair import Pair


class TestMatchClass:
    def test_instantiation(self, random_candidate_dict, random_role_dict):
        c = Candidate(**random_candidate_dict())
        r = Role(**random_role_dict())
        m = Matching([c], [r], Pair)
        assert m

    def test_large_instantiation(self, random_candidates, random_roles):
        m = Matching(random_candidates, random_roles, Pair)
        assert m

    def test_match_process_works(self, random_candidates, random_roles):
        m = Matching(random_candidates, random_roles, Pair)
        pairs = m._match()
        assert pairs

    def test_reject_impossible_roles(self, random_candidates, random_roles):
        with patch(
            "fast_stream_22.matching.match.Matching._score_or_disqualify",
            return_value=DISALLOWED,
        ):
            m = Matching(random_candidates, random_roles, Pair)
            assert m.reject_impossible_roles() == random_roles
