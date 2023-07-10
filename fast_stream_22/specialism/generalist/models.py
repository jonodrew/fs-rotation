from __future__ import annotations

from functools import wraps
from typing import Callable, Optional
from fast_stream_22.specialism.pair import BasePair
from fast_stream_22.specialism.models import Travel, Clearance, Cohort, Candidate, Role
from fast_stream_22.specialism.pair import register_scoring_method, C, R


class WorkingPatternsInterface:
    def __init__(self, working_patterns: str, **kwargs):
        self._working_patterns = {
            pattern.strip() for pattern in working_patterns.split(",")
        }
        super().__init__(**kwargs)

    @property
    def working_patterns(self):
        return self._working_patterns


class AccessibilityInterface:
    def __init__(self, accessibility: str, **kwargs):
        self._accessibility = {
            requirement.strip() for requirement in accessibility.split(",")
        }
        super().__init__(**kwargs)


class GeneralistCandidate(WorkingPatternsInterface, AccessibilityInterface, Candidate):
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
        match_pref_1: str = None,
        match_pref_2: str = None,
        **kwargs,
    ):
        kwargs["prior_departments"] = kwargs["prior_departments"].replace(" ", ",")
        kwargs["working_patterns"] = kwargs["preferred_office_attendance"]
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

        if self.year_group == Cohort.SixMonth:
            self.can_relocate = False

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

    @property
    def accessibility_needs(self):
        return self._accessibility


class GeneralistRole(WorkingPatternsInterface, AccessibilityInterface, Role):
    def __init__(self, anchor: str, **kwargs):
        kwargs["working_patterns"] = kwargs["office_arrangement"]
        super().__init__(**kwargs)
        self.anchor = anchor
        if Cohort.Two in self.suitable_year_groups:
            self.suitable_year_groups.add(Cohort.SixMonth)

    @property
    def accessibility_adjustment(self):
        return self._accessibility


def register_method_called(
    func: Callable[["GeneralistPair"], None]
) -> Callable[["GeneralistPair"], None]:
    @wraps(func)
    def _inner(instance: GeneralistPair) -> None:
        before_score = instance.score
        func(instance)
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

    def __init__(self, candidate: C, role: R):
        super().__init__(candidate, role)
        self.methods_called: set[Optional[str]] = set()

    @register_scoring_method
    def _check_accessibility(self) -> None:
        """
        Check whether the accessibility needs of the Candidate are a subset (ie, contained within) the accessibility
        adjustments offered by the Role

        :return:
        """
        self.disqualified = not self.candidate.accessibility_needs.issubset(
            self.role.accessibility_adjustment
        )

    @register_scoring_method
    def _check_travel(self) -> None:
        """
        Disqualify candidates whose travel requirements don't match those in the role

        :return: None
        """
        self.disqualified = (
            self.role.travel_requirements > self.candidate.travel_requirements
        )

    @register_scoring_method
    def _check_prior_departments(self) -> None:
        """
        In the Generalist scheme, candidates are disqualified from visiting a department they've previously visited

        :return: None
        """
        self.disqualified = self.role.department in self.candidate.prior_departments

    @register_scoring_method
    def _check_working_pattern(self) -> None:
        """
        We compare the role's required working pattern with the candidate preferences. If there is no overlap, this
        marks the match as disqualified. The candidate is allowed to select one preferred working patterns, while the
        role can offer any number of roles.

        :return: None
        """
        self.disqualified = not self.candidate.working_patterns.issubset(
            self.role.working_patterns
        )

    @register_scoring_method
    @register_method_called
    def _score_department(self) -> None:
        if self.role.department in self.candidate.dept_prefs:
            self._score += self.scoring_weights["department"]

    @register_scoring_method
    @register_method_called
    def _score_anchor(self) -> None:
        if self.role.anchor in {
            self.candidate.primary_anchor,
            self.candidate.secondary_anchor,
        }:
            self._score += self.scoring_weights["anchor"]

    @register_method_called
    @register_scoring_method
    def _score_skill(self) -> None:
        return super()._score_skill()

    @register_method_called
    @register_scoring_method
    def _score_location(self) -> None:
        return super()._score_location()

    def _score_preferences(self):
        preferences = {
            "Anchor": self._score_anchor.__name__,
            "Location": self._score_location.__name__,
            "Department": self._score_department.__name__,
            "Skill": self._score_skill.__name__,
        }
        for preference in self.candidate.match_preferences:
            if preferences.get(preference) in self.methods_called:
                self._score += self.scoring_weights["preference"]

    def score_pair(self) -> int:
        super().score_pair()
        self._score_preferences()
        return self.score
