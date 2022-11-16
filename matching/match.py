from __future__ import annotations

from functools import partial
from typing import Callable, Sequence, Iterable, Union
from munkres import DISALLOWED, make_cost_matrix, Munkres
from numpy import ndarray

from matching.read_in import read_candidates, read_roles
from matching.scoring import score_skills, score_location, score_clearance
from matching.models import Candidate, Role
import numpy as np

ScoringFunc = Callable[[Candidate, Role], int]


def get_candidate_and_role_pair(candidate_i: int, role_i: int) -> tuple[Candidate, Role]:
    return read_candidates()[candidate_i], read_roles()[role_i]


def generate_grid(candidates: Sequence[Candidate], roles: Sequence[Role]) -> ndarray[int]:
    match_func = partial(_match_candidate_to_role, {score_skills: 1, score_location: 1, score_clearance: 9})
    arr = np.array([match_func(c, r) for r in roles for c in candidates])
    return np.reshape(arr, (len(candidates), len(roles)))


def process_matches(matrix: list[list[Union[DISALLOWED, int]]]) -> Iterable[tuple[int, int]]:
    yield from Munkres().compute(make_cost_matrix(matrix))


def _disallow_blocked(matrix: ndarray[int]) -> ndarray[int | DISALLOWED]:
    return np.vectorize(lambda x: DISALLOWED if x < 0 else x)(matrix)


def prepare_grid(matrix: ndarray[int]) -> list[list[DISALLOWED | int]]:
    return _disallow_blocked(matrix).tolist()  # type: ignore


def _match_candidate_to_role(func_weight_map: dict[ScoringFunc, int], c: Candidate, r: Role) -> int:
    def _scores():
        return map(lambda f_w: f_w[0](c, r) * f_w[1], func_weight_map.items())

    if any(map(lambda s: s < 0, _scores())):
        return -1
    else:
        return sum(_scores())

