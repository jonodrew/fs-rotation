from __future__ import annotations

import dataclasses
import datetime
import functools
import logging
import sys
from collections import defaultdict
from typing import (
    Sequence,
    Union,
    TypeVar,
    Optional,
    Type,
)
from munkres import DISALLOWED, make_cost_matrix, Munkres, UnsolvableMatrix

from fast_stream_22.matching.models import Candidate, Role, BaseClass
from fast_stream_22.matching.pair import Pair, R, C, P
import numpy as np

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Bid:
    cohort: int
    _department: str
    number: int = 0
    count: int = 0
    initial_round_percentage: float = 0.8

    @property
    def min_number(self):
        if self.number in {0, 1}:
            return self.number
        elif self.number < 5:
            return self.number - 1
        else:
            return round(self.number * self.initial_round_percentage)

    @property
    def department(self):
        return self._department.lower()


Result = tuple[str, str, int]


class Process:
    def __init__(
        self,
        all_candidates: Sequence[Candidate],
        all_roles: Sequence[Role],
        bids: Sequence[Bid],
        senior_to_junior: bool = False,
        pair_type: Type[P] = Pair,  # type: ignore
    ):
        self._all_candidates = all_candidates
        self.candidate_mapping: dict[str, Candidate] = {
            c.uid: c for c in all_candidates
        }
        self._all_roles = all_roles
        self.all_roles_mapping: dict[str, Role] = {r.uid: r for r in all_roles}
        self.bids = bids
        self.pairings: dict[int, list[Result]] = defaultdict(list)
        self.max_rounds = 5
        self.senior_to_junior = senior_to_junior
        self.specialism = pair_type

    def _compute_cohort(self, cohort: int):
        if self.match_cohort(cohort):
            logger.info(f"Successfully matched cohort {cohort}")
        else:
            logger.info(f"Cohort {cohort} could not be perfectly matched")
        self.reset_roles()
        for pair in self.pairings[cohort]:
            logger.info(f"{','.join(map(str, pair))}")

    def compute(self):
        """
        Try to solve each cohort in turn. The order is defined in self.senior_to_junior. When finished, unmark any roles
        that were rejected, as they may be suitable for the next cohort.

        :return:
        """
        cohorts = sorted(
            set((bid.cohort for bid in self.bids)), reverse=self.senior_to_junior
        )
        for cohort in cohorts:
            self._compute_cohort(cohort)
        total_bids = 0
        total_count = 0
        dept_bids_mapping = defaultdict(list)
        for bid in self.bids:
            dept_bids_mapping[bid.department].append(bid)
            total_bids += bid.number
        all_min_bids = 0
        logger.info("bids/count")
        for dept, bids in dept_bids_mapping.items():
            bids_matches = ",".join([f"{bid.number},{bid.count}" for bid in bids])
            logger.info(f"{dept},{bids_matches}")
            min_bids = sum([b.min_number for b in bids])
            all_min_bids += min_bids
            this_count = sum([b.count for b in bids])
            total_count += this_count
        logger.info(
            f"There were {total_bids} bids in total against {total_count} total"
            " candidates"
        )

    def reset_roles(self):
        """
        Mark all roles as matchable

        :return:
        """
        for r in self._all_roles:
            r.no_match = False
        logger.info("Roles reset")

    @property
    def all_candidates(self) -> list[Candidate]:
        """
        Get all candidates that haven't been paired

        :return: a list of unpaired candidates
        """
        return self.mask_paired(self._all_candidates)

    @property
    def all_roles(self) -> list[Role]:
        """
        Get all the roles that haven't been paired and haven't been marked as 'rejected'

        :return: a list of unpaired, unrejected roles
        """
        return sorted(
            self.mask_paired([r for r in self._all_roles if not r.no_match]),
            key=lambda role: role.priority_role,
            reverse=True,
        )

    Pairable = TypeVar("Pairable", bound=BaseClass)

    @staticmethod
    def mask_paired(data: Sequence[Pairable]) -> list[Pairable]:
        """
        Hide the data that's already been paired

        :param data: a sequence of Pairable objects
        :return: a list of Pairable objects that haven't yet been paired
        """
        return [data_point for data_point in data if not data_point.paired]

    def pair_off(
        self, candidates: Sequence[Candidate], roles: Sequence[Role]
    ) -> list[tuple[str, str]]:
        """
        Create a round of Matching, compute it, and return the pairs

        :param candidates: this cohort's candidates
        :param roles: the potential set of roles
        :return: a list of paired candidate/role
        """
        return Matching(candidates, roles, self.specialism).report_pairs()

    @functools.lru_cache
    def _cohort_bids(self, cohort: int) -> dict[str, Bid]:
        return {bid.department: bid for bid in self.bids if bid.cohort == cohort}

    def _prepare_round(
        self, cohort: int, round_number: int
    ) -> tuple[list[Candidate], list[Role]]:
        """
        Prepare the inputs for a round of matching. If this is the zeroth round, limit roles to be put forward to 80% of
        a department's total bid. After that, put forward (bids - awarded) bids from each department

        :param cohort: an integer describing the cohort
        :param round_number: the number for this round
        :return: a tuple, consisting of a list of candidates and a list of roles
        """
        cohort_bids = self._cohort_bids(cohort)
        candidates = [c for c in self.all_candidates if c.year_group == cohort]
        suitable_roles = [
            role for role in self.all_roles if cohort in role.suitable_year_groups
        ]
        shortlisted_roles = []
        for bid in sorted(
            cohort_bids.values(), key=lambda bid: bid.number, reverse=False
        ):
            if round_number == 0:
                shortlist_length = bid.min_number
            else:
                shortlist_length = bid.number - bid.count
            shortlisted_roles.extend(
                [role for role in suitable_roles if role.department == bid.department][
                    :shortlist_length
                ]
            )
        return candidates, shortlisted_roles

    def match_cohort(
        self, cohort: int, round_number: int = 0, failures: int = 0
    ) -> bool:
        """
        This method takes a cohort and tries to match the candidates to potential roles. Where matches are made, bids
        are reduced. This means that once a department has met its quota it no longer gets to put roles in for matching

        :param cohort: the year group we're matching
        :param round_number: the number of times we've tried this
        :param failures: the number of failures from this cohort
        :return: a boolean signifying if we were successful
        """
        cohort_bids = self._cohort_bids(cohort)
        if failures > 20:
            raise Exception("Too many failures")
        if round_number >= self.max_rounds:
            logger.info("Too many rounds!")
            return all(
                map(lambda bid: bid.count >= bid.min_number, cohort_bids.values())
            )
        candidates, shortlisted_roles = self._prepare_round(cohort, round_number)
        if not shortlisted_roles:
            raise Exception("No roles left to try!")
        this_round = Matching(candidates, shortlisted_roles, self.specialism)
        if rejects := this_round.reject_impossible_roles():
            logger.info(f"Attempt #{failures}: Failed to find enough roles")
            logger.info(f"Rejected following roles: {','.join(map(str, rejects))}")
            return self.match_cohort(cohort, round_number, failures + 1)
        pairs = self.pair_off(candidates, shortlisted_roles)
        pair_scores: list[Result] = []
        for candidate_id, role_id in pairs:
            self.candidate_mapping[candidate_id].mark_paired()
            role = self.all_roles_mapping[role_id]
            role.mark_paired()
            cohort_bids[role.department].count += 1
            pair_scores.append(
                (
                    candidate_id,
                    role_id,
                    self.specialism().score_pair(
                        self.candidate_mapping[candidate_id], role
                    ),
                )
            )

        self.pairings[cohort].extend(pair_scores)
        if len(pairs) == len(candidates):
            return True
        else:
            logger.info(
                f"Round {round_number} failed. {len(candidates) - len(pairs)} still to"
                f" pair ({[c for c in candidates if not c.paired]}"
            )
            return self.match_cohort(cohort, round_number + 1)


class Matching:
    def __init__(
        self, candidates: Sequence[Candidate], roles: Sequence[Role], pair_type: Type[P]
    ):
        self.candidates = candidates
        self.roles = roles
        self.pairs = [
            self._score_or_disqualify(pair_type(), c, r)
            for c in candidates
            for r in roles
        ]
        self.score_grid = np.reshape(self.pairs, (len(candidates), len(roles)))

    def reject_impossible_roles(self) -> list[Optional[Role]]:
        """
        Identify and reject roles that no candidate can do

        :return: a list of rejected roles
        """
        rejects = []
        for i, column in enumerate(self.score_grid.T):
            if np.all(column == DISALLOWED):
                rejects.append(self.roles[i])
                self.roles[i].no_match = True
                logger.info(f"No candidate could be found for role {self.roles[i]}")
        return rejects

    @staticmethod
    def _score_or_disqualify(p: P, candidate: C, role: R) -> Union[DISALLOWED, int]:
        p.score_pair(candidate, role)
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
        try:
            pairs = self._match()
            return [self._convert_pair(p) for p in pairs]
        except UnsolvableMatrix:
            log_copy = self.score_grid.copy()
            log_copy[log_copy == DISALLOWED] = "D"
            np.savetxt(
                f"{datetime.datetime.utcnow()}-log.csv",
                log_copy,
                delimiter=",",
                fmt="%s",
            )
            raise UnsolvableMatrix

    def _convert_pair(self, pair: tuple[int, int]) -> tuple[str, str]:
        candidate, role = pair
        return self.candidates[candidate].uid, self.roles[role].uid
