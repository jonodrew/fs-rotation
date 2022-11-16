import functools
from unittest.mock import patch
from matching.match import process_matches, generate_grid, prepare_grid, get_candidate_and_role_pair
from matching.models import Candidate, Clearance, Role


@functools.lru_cache
def _candidates():
    return [
        Candidate("Aisha", Clearance.SC, "", {"Digital": 4, "Policy": 2, "Operations": 1, "Finance": 0}, "", True,
                  [""]),
        Candidate("Benjamin", Clearance.SC, "", {"Digital": 1, "Policy": 2, "Operations": 3, "Finance": 4}, "", True,
                  [""])
    ]


@functools.lru_cache
def _roles():
    return [
        Role("Assistant Head of Finance", Clearance.SC, "", {"Digital": 1, "Policy": 1, "Operations": 0, "Finance": 5}, ""),
        Role("Delivery Manager", Clearance.SC, "", {"Digital": 4, "Policy": 1, "Operations": 2, "Finance": 0}, ""),
    ]


@patch("matching.match.read_roles", return_value=_roles())
@patch("matching.match.read_candidates", return_value=_candidates())
class TestMatch:

    def test_end_to_end(self, patched_candidates, patched_roles):
        pairs = list(
                map(lambda c_r: get_candidate_and_role_pair(*c_r),
                    process_matches(prepare_grid(generate_grid(_candidates(), _roles())))))

        assert pairs[0] == (_candidates()[0], _roles()[0])
        assert pairs[1] == (_candidates()[1], _roles()[1])
