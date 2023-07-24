import logging
import os
from functools import wraps
from typing import Callable, TypeVar, Generic

from fast_stream_22.specialism.models import Candidate, Role, Cohort

P = TypeVar("P", bound="BasePair")
C = TypeVar("C", bound=Candidate)
R = TypeVar("R", bound=Role)

logger = logging.getLogger(__name__)


def register_scoring_method(func: Callable[[P], None]) -> Callable[[P], None]:
    func._is_scoring_method = True  # type: ignore

    @wraps(func)
    def inner(instance: P) -> None:
        before = instance.disqualified
        score_before = instance.score
        func(instance)
        if os.environ.get("DEBUG") == "true":
            if instance.disqualified is True and before is False:
                logger.debug(
                    f"{instance.candidate} dq'd from {instance.role} because of"
                    f" {func.__name__}"
                )
            elif score_before < instance.score:
                logger.debug(
                    f"{instance.candidate} scored with {instance.role} thanks to"
                    f" {func.__name__}"
                )
        return None

    return inner


class BasePair(Generic[C, R]):
    scoring_method_names: set[str] = set()

    scoring_weights: dict[str, int] = {
        "first_location": 10,
        "second_location": 5,
        "department": 10,
        "skill": 20,
        "stretch": 10,
        "year_appropriate": 5,
        "has_relocated": 10,
    }
    min_score: dict[int, int] = {Cohort.One: 15, Cohort.Two: 20, Cohort.Three: 25}

    def __init_subclass__(cls, **kwargs):
        cls.scoring_method_names = set()
        for name in dir(cls):
            if getattr(getattr(cls, name), "_is_scoring_method", False):
                cls.scoring_method_names.add(name)
        super().__init_subclass__()

    def __init__(self, candidate: C, role: R):
        self.candidate = candidate
        self.role = role
        self._score: int = 0
        self._disqualified = False

    @property
    def scoring_methods(self) -> set[Callable[[], None]]:
        """
        Collect the methods marked for scoring for this class

        :return: a set of callable methods
        """
        return {getattr(self, name) for name in self.scoring_method_names}

    def score_pair(self) -> int:
        """
        Run through the scoring methods for this class

        :return: an int representing the final score for this Pair
        """
        for method in self.scoring_methods:
            method()
            if self.disqualified:
                return self.score
        self._check_score()
        return self.score

    @register_scoring_method
    def _check_location(self) -> None:
        """
        If a candidate can't relocate, then a Role should be disqualified if both of the following are False:
        * the Role can be done from anywhere
        * the Candidate's first or second preference locations are in the Role's locations

        :return:
        """
        candidate_cannot_relocate = not self.candidate.can_relocate
        if candidate_cannot_relocate:
            role_in_good_location: bool = self.role.from_anywhere() or not {
                self.candidate.first_preference_location,
                self.candidate.second_preference_location,
            }.isdisjoint(self.role.locations)
            self._disqualified = not role_in_good_location

    @register_scoring_method
    def _score_location(self) -> None:
        if self.candidate.has_relocated:
            self.scoring_weights["first_location"] += self.scoring_weights[
                "has_relocated"
            ]
            self.scoring_weights["second_location"] += self.scoring_weights[
                "has_relocated"
            ]

        if self.role.from_anywhere():
            self._score += self.scoring_weights["first_location"]
        elif (
            self.candidate.first_preference_location in self.role.locations
            or self.candidate.first_preference_location == "Any"
        ):
            self._score += self.scoring_weights["first_location"]
        elif (
            self.candidate.second_preference_location in self.role.locations
            or self.candidate.second_preference_location == "Any"
        ):
            self._score += self.scoring_weights["second_location"]

    @register_scoring_method
    def _check_clearance(self) -> None:
        self.disqualified = self.candidate.clearance < self.role.clearance

    @register_scoring_method
    def _check_nationality(self) -> None:
        """
        Nationality requirements come in three flavours: British national only, dual national, no restriction

        :return:
        """
        self.disqualified = (
            self.role.nationality_requirement > self.candidate.british_national
        )

    @register_scoring_method
    def _check_passport(self) -> None:
        self.disqualified = (
            self.role.passport_requirement and not self.candidate.has_passport
        )

    @register_scoring_method
    def _check_year_group(self) -> None:
        self.disqualified = (
            self.candidate.year_group not in self.role.suitable_year_groups
        )

    @register_scoring_method
    def _check_ethics(self) -> None:
        self.disqualified = (
            self.candidate.no_immigration and self.role.immigration_role
        ) or (self.candidate.no_defence and self.role.defence_role)

    @register_scoring_method
    def _check_stretch(self) -> None:
        if (
            not self.candidate.wants_private_office and self.role.private_office_role
        ) or (
            not self.candidate.wants_line_management and self.role.line_management_role
        ):
            self.disqualified = True

    @register_scoring_method
    def _score_stretch(self) -> None:
        if self.candidate.wants_private_office and self.role.private_office_role:
            self._score += self.scoring_weights["stretch"]
        if self.candidate.wants_line_management and self.role.line_management_role:
            self._score += self.scoring_weights["stretch"]

    @register_scoring_method
    def _score_year_only(self) -> None:
        """
        If a role is only suitable for one year group, score it more highly

        :return: None
        """
        year_groups = self.role.suitable_year_groups
        if len(year_groups) == 1 and self.candidate.year_group in year_groups:
            self._score += self.scoring_weights["year_appropriate"]

    @register_scoring_method
    def _score_department(self) -> None:
        if self.role.department not in self.candidate.prior_departments:
            self._score += self.scoring_weights["department"]

    @register_scoring_method
    def _score_skill(self) -> None:
        if self.role.secondary_focus == self.candidate.last_role_secondary_skill:
            self._score -= 5
        bonus = self.scoring_weights["skill"]
        for skill in (self.candidate.primary_skill, self.candidate.secondary_skill):
            for focus in (self.role.skill_focus, self.role.secondary_focus):
                if skill == focus:
                    self._score += bonus
                bonus -= 5

    def _check_score(self) -> None:
        """
        The lowest acceptable score for a match. If the score is too low, set `self.disqualified` to `True`

        :return:
        """
        if not self.score >= self.min_score.get(self.candidate.year_group, 0):
            self.disqualified = True

    @property
    def disqualified(self) -> bool:
        return self._disqualified

    @disqualified.setter
    def disqualified(self, value: bool) -> None:
        if self._disqualified or value:
            self._disqualified = True
        else:
            self._disqualified = False

    @property
    def score(self) -> int:
        return self._score


class Pair(BasePair):
    pass
