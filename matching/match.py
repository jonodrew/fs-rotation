from __future__ import annotations

from typing import Sequence, Union
from munkres import DISALLOWED, make_cost_matrix, Munkres

from matching.models import Candidate, Role, Pair
import numpy as np


class Matching:
    def __init__(self, candidates: Sequence[Candidate], roles: Sequence[Role]):
        self.pairs = [Pair(c, r) for c in candidates for r in roles]
        self.grid = np.reshape(self.pairs, (len(candidates), len(roles)))
        self.score_grid = self.generate_score_grid()

    @staticmethod
    def _score_or_disqualify(p: Pair) -> Union[DISALLOWED, int]:
        if p.disqualified:
            return DISALLOWED
        else:
            return p.score

    def generate_score_grid(self):
        v_func = np.vectorize(self._score_or_disqualify)
        return v_func(self.grid)

    def match(self):
        matrix = make_cost_matrix(self.score_grid)
        return Munkres().compute(matrix)
