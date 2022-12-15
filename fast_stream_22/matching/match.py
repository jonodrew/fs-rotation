from __future__ import annotations

import itertools
import sys
from typing import Sequence, Union, Optional
from munkres import DISALLOWED, make_cost_matrix, Munkres

from fast_stream_22.matching.models import Candidate, Role, Pair
import numpy as np


class Process:
    def __init__(
        self,
        candidates: Sequence[Candidate],
        all_roles: Sequence[Role],
        bids: dict[str, int] = None,
    ):
        self.candidates = candidates
        self.all_roles = all_roles
        self.bids = bids
        self.pairings: Optional[list[tuple[str, str]]] = None

    def _filter_roles(self, department: str, bids: int) -> list[Role]:
        """
        Return as many roles as the department has bid for.

        :param department: the department we need to filter
        :param bids: the number of bids they've made
        :return: a filtered list of the highest priority roles, with length `bids`
        """
        departmental_roles = filter(
            lambda r: r.department == department, self.all_roles
        )
        sort_by_priority = sorted(
            departmental_roles, key=lambda role: role.priority_role
        )
        return sort_by_priority[:bids]

    def _first_round(self):
        first_round_roles = list(
            itertools.chain(
                *[self._filter_roles(dept, bid_count) for dept, bid_count in self.bids]
            )
        )
        self.pairings = Matching(self.candidates, first_round_roles).report_pairs()
        return len(self.pairings) == len(self.candidates)

    def pair_off(self):
        if self.bids is None:
            self.pairings = Matching(self.candidates, self.all_roles).report_pairs()
        else:
            if not self._first_round():
                second_round_roles = [
                    role
                    for role in self.all_roles
                    if role.uid not in (pair[1] for pair in self.pairings)
                ]
                second_round_candidates = [
                    candidate
                    for candidate in self.candidates
                    if candidate.uid not in (pair[0] for pair in self.pairings)
                ]
                second_round_pairings = Matching(
                    second_round_candidates, second_round_roles
                ).report_pairs()
                if len(second_round_pairings) + len(self.pairings) != self.candidates:
                    raise Exception
                else:
                    self.pairings.extend(second_round_pairings)
        return self.pairings


class Matching:
    def __init__(self, candidates: Sequence[Candidate], roles: Sequence[Role]):
        self.candidates = candidates
        self.roles = roles
        self.pairs = [
            self._score_or_disqualify(Pair(c, r)) for c in candidates for r in roles
        ]
        self.score_grid = np.reshape(self.pairs, (len(candidates), len(roles)))

    @staticmethod
    def _score_or_disqualify(p: Pair) -> Union[DISALLOWED, int]:
        p.score_pair()
        if p.disqualified:
            return DISALLOWED
        else:
            return p.score

    def _match(self):
        matrix = make_cost_matrix(
            self.score_grid, lambda x: sys.maxsize - x if type(x) is int else x
        )
        return Munkres().compute(matrix)

    def report_pairs(self) -> list[tuple[str, str]]:
        """
        :return: Return a list of tuples, representing the candidate-role pairings

        """
        pairs = self._match()
        return [self._convert_pair(p) for p in pairs]

    def _convert_pair(self, pair: tuple[int, int]) -> tuple[str, str]:
        candidate, role = pair
        return self.candidates[candidate].uid, self.roles[role].uid
