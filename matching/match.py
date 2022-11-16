from __future__ import annotations

from functools import partial
from typing import Callable, Sequence, Iterable
from munkres import DISALLOWED, make_cost_matrix, Munkres
from numpy import ndarray

from matching.read_in import read_candidates, read_roles
from matching.scoring import score_skills, score_location
from models import Candidate, Role
import numpy as np

ScoringFunc = Callable[[Candidate, Role], int]


def get_candidate_and_role_pair(candidate_i: int, role_i: int) -> tuple[Candidate, Role]:
    return read_candidates()[candidate_i], read_roles()[role_i]


def generate_grid(candidates: Sequence[Candidate], roles: Sequence[Role]) -> ndarray[int]:
    match_func = partial(match_candidate_to_role, func_weight_map={score_skills: 1, score_location: 1})
    arr = np.array([match_func(c, r) for r in roles for c in candidates])
    return np.reshape(arr, (len(candidates), len(roles)))


def process_matches(matrix: list[list[DISALLOWED | int]]) -> Iterable[tuple[int, int]]:
    yield from Munkres().compute(make_cost_matrix(matrix))


def _disallow_blocked(matrix: ndarray[int]) -> ndarray[int | DISALLOWED]:
    return np.vectorize(lambda x: DISALLOWED if x < 0 else x)(matrix)


def prepare_grid(matrix: ndarray[int]) -> list[list[DISALLOWED | int]]:
    return _disallow_blocked(matrix).tolist()  # type: ignore


def match_candidate_to_role(c: Candidate, r: Role, func_weight_map: dict[ScoringFunc, int]) -> int | DISALLOWED:
    if not all(map(lambda f, weight: weight * f(c, r), func_weight_map.items())):
        return DISALLOWED
    else:
        return sum(map(lambda f, weight: weight * f(c, r), func_weight_map.items()))
