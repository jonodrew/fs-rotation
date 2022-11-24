from matching.match import Matching
from matching.models import Candidate, Role


class TestMatchClass:
    def test_instantiation(self, random_candidate_dict, random_role_dict):
        c = Candidate(**random_candidate_dict())
        r = Role(**random_role_dict())
        m = Matching([c], [r])
        assert m

    def test_large_instantiation(self, random_candidates, random_roles):
        m = Matching(random_candidates, random_roles)
        assert m
