from typing import Callable, TypeVar

from fast_stream_22.matching.models import Candidate, Role


P = TypeVar("P", bound="BasePair")


def register_scoring_method(func: Callable[[P], None]) -> Callable[[P], None]:
    func._is_scoring_method = True  # type: ignore
    return func


C = TypeVar("C", bound=Candidate)
R = TypeVar("R", bound=Role)


class BasePair:
    scoring_method_names: set[str] = set()

    def __init_subclass__(cls, **kwargs):
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
        self._check_score()
        return self._score

    def _check_score(self) -> None:
        """
        The lowest acceptable score for a match. If the score is too low, set `self.disqualified` to `True`

        :return:
        """
        raise NotImplementedError

    @property
    def disqualified(self):
        return self._disqualified

    @disqualified.setter
    def disqualified(self, value: bool):
        if self._disqualified or value:
            self._disqualified = True
        else:
            self._disqualified = False

    @property
    def score(self):
        return self._score


class Pair(BasePair):
    scoring_weights: dict[str, int] = {
        "first_location": 10,
        "second_location": 5,
        "department": 10,
        "skill": 20,
        "stretch": 10,
    }

    @register_scoring_method
    def _check_location(self):
        if not self.candidate.can_relocate:
            self._disqualified = not (
                self.role.from_anywhere()
                or self.candidate.first_preference_location in self.role.locations
                or self.candidate.second_preference_location in self.role.locations
            )

    @register_scoring_method
    def _score_location(self):
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
    def _score_clearance(self):
        self.disqualified = self.candidate.clearance < self.role.clearance

    @register_scoring_method
    def _check_nationality(self):
        """
        Nationality requirements come in three flavours: British national only, dual national, no restriction

        :return:
        """
        self.disqualified = (
            self.role.nationality_requirement > self.candidate.british_national
        )

    @register_scoring_method
    def _check_passport(self):
        self.disqualified = (
            self.role.passport_requirement and not self.candidate.has_passport
        )

    @register_scoring_method
    def _score_department(self):
        if self.role.department not in self.candidate.prior_departments:
            self._score += self.scoring_weights["department"]

    @register_scoring_method
    def _ethical_check(self):
        self.disqualified = (
            self.candidate.no_immigration and self.role.immigration_role
        ) or (self.candidate.no_defence and self.role.defence_role)

    @register_scoring_method
    def _appropriate_for_year_group(self):
        self.disqualified = (
            self.candidate.year_group not in self.role.suitable_year_groups
        )

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

    @register_scoring_method
    def _stretch_check(self):
        if (
            not self.candidate.wants_private_office and self.role.private_office_role
        ) or (
            not self.candidate.wants_line_management and self.role.line_management_role
        ):
            self.disqualified = True
        else:
            if self.candidate.wants_private_office and self.role.private_office_role:
                self._score += self.scoring_weights["stretch"]
            if self.candidate.wants_line_management and self.role.line_management_role:
                self._score += self.scoring_weights["stretch"]

    def _check_score(self):
        if self.score < 20:
            self.disqualified = True
