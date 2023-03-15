from __future__ import annotations

from functools import wraps
from typing import Callable
from fast_stream_22.matching.pair import BasePair
from fast_stream_22.matching.models import Travel, Clearance, Cohort, Candidate, Role
from fast_stream_22.matching.pair import register_scoring_method, C, R


class GeneralistCandidate(Candidate):
    def __init__(
        self,
        primary_anchor_seeking: str,
        secondary_anchor_seeking: str,
        dept_pref_1: str,
        dept_pref_2: str,
        dept_pref_3: str,
        dept_pref_4: str,
        dept_pref_5: str,
        travel_requirements: str,
        accessibility: str = None,
        match_pref_1: str = None,
        match_pref_2: str = None,
        **kwargs,
    ):
        kwargs["prior_departments"] = kwargs["prior_departments"].replace(" ", ",")
        super().__init__(**kwargs)
        self.match_preferences = {match_pref_2, match_pref_1}
        self.primary_anchor = primary_anchor_seeking
        self.secondary_anchor = secondary_anchor_seeking
        self.dept_prefs = {
            self._stringify_department(dept)
            for dept in [
                dept_pref_1,
                dept_pref_2,
                dept_pref_3,
                dept_pref_4,
                dept_pref_5,
            ]
        }
        self.travel_requirements: Travel = Travel.factory(travel_requirements)
        self._fix_previous_departments()

    def _fix_previous_departments(self):
        """
        Scottish and Welsh government are so varied that Candidates can visit them again, so we remove them as a 'prior
        department' if `self.can_relocate` is False

        :return:
        """
        if not self.can_relocate:
            for department in ("wg", "sg"):
                self.prior_departments.discard(department)

    @property
    def clearance(self) -> Clearance:
        return super().clearance if self._clearance != Clearance.DV else Clearance.SC


class GeneralistRole(Role):
    def __init__(self, accessibility: str, anchor: str, **kwargs):
        super().__init__(**kwargs)
        self.accessibility = accessibility
        self.anchor = anchor
        if Cohort.Two in self.suitable_year_groups:
            self.suitable_year_groups.add(Cohort.SixMonth)


def register_method_called(
    func: Callable[["GeneralistPair", C, R], None]
) -> Callable[["GeneralistPair", C, R], None]:
    @wraps(func)
    def _inner(instance: GeneralistPair, candidate: C, role: R) -> None:
        before_score = instance.score
        func(instance, candidate, role)
        if instance.score > before_score:
            instance.methods_called.add(func.__name__)
        return None

    return _inner


class GeneralistPair(BasePair):
    scoring_weights = {
        **BasePair.scoring_weights,
        "anchor": 15,
        "preference": 10,
    }

    min_score = {
        **BasePair.min_score,
        Cohort.SixMonth: BasePair.min_score[Cohort.Two],
    }

    def __init__(self):
        super().__init__()
        self.methods_called = set()

    @register_scoring_method
    def _check_travel(self, c: GeneralistCandidate, r: GeneralistRole) -> None:
        """
        Disqualify candidates whose travel requirements don't match those in the role

        :param c: the Candidate
        :param r: the Role
        :return: None
        """
        self.disqualified = r.travel_requirements > c.travel_requirements

    @register_scoring_method
    def _check_prior_departments(
        self, c: GeneralistCandidate, r: GeneralistRole
    ) -> None:
        """
        In the Generalist scheme, candidates are disqualified from visiting a department they've previously visited

        :param c: the Candidate
        :param r: the Role
        :return: None
        """
        self.disqualified = r.department in c.prior_departments

    @register_scoring_method
    @register_method_called
    def _score_department(
        self, candidate: GeneralistCandidate, role: GeneralistRole
    ) -> None:
        if role.department in candidate.dept_prefs:
            self._score += self.scoring_weights["department"]

    @register_scoring_method
    @register_method_called
    def _score_anchor(self, c: GeneralistCandidate, r: GeneralistRole) -> None:
        if r.anchor in {c.primary_anchor, c.secondary_anchor}:
            self._score += self.scoring_weights["anchor"]

    @register_method_called
    @register_scoring_method
    def _score_skill(self, candidate: C, role: R) -> None:
        return super()._score_skill(candidate, role)

    @register_method_called
    @register_scoring_method
    def _score_location(self, candidate: C, role: R) -> None:
        return super()._score_location(candidate, role)

    def _score_preferences(self, candidate: GeneralistCandidate):
        preferences = {
            "Anchor": self._score_anchor.__name__,
            "Location": self._score_location.__name__,
            "Department": self._score_department.__name__,
            "Skill": self._score_skill.__name__,
        }
        for preference in candidate.match_preferences:
            if preferences.get(preference) in self.methods_called:
                self._score += self.scoring_weights["preference"]

    def score_pair(self, candidate: GeneralistCandidate, role: GeneralistRole) -> int:
        super().score_pair(candidate, role)
        self._score_preferences(candidate)
        return self.score
