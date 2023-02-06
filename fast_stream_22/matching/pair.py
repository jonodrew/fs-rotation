from typing import Callable, TypeVar

from fast_stream_22.matching.models import Candidate, Role


P = TypeVar("P", bound="BasePair")
C = TypeVar("C", bound=Candidate)
R = TypeVar("R", bound=Role)


def register_scoring_method(
    func: Callable[[P, C, R], None]
) -> Callable[[P, C, R], None]:
    func._is_scoring_method = True  # type: ignore
    return func


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
    def scoring_methods(self) -> set[Callable[[C, R], None]]:
        """
        Collect the methods marked for scoring for this class

        :return: a set of callable methods
        """
        return {getattr(self, name) for name in self.scoring_method_names}

    def score_pair(self, candidate=None, role=None) -> int:
        """
        Run through the scoring methods for this class

        :param candidate:
        :param role:
        :return: an int representing the final score for this Pair
        """
        for method in self.scoring_methods:
            method(self.candidate, self.role)
        self._check_score()
        return self._score

    scoring_weights: dict[str, int] = {
        "first_location": 10,
        "second_location": 5,
        "department": 10,
        "skill": 20,
        "stretch": 10,
    }

    @register_scoring_method
    def _check_location(self, candidate: C, role: R) -> None:
        if not candidate.can_relocate:
            self._disqualified = not (
                role.from_anywhere()
                or candidate.first_preference_location in role.locations
                or candidate.second_preference_location in role.locations
            )

    @register_scoring_method
    def _score_location(self, candidate: C, role: R) -> None:
        if role.from_anywhere():
            self._score += self.scoring_weights["first_location"]
        elif (
            candidate.first_preference_location in role.locations
            or candidate.first_preference_location == "Any"
        ):
            self._score += self.scoring_weights["first_location"]
        elif (
            candidate.second_preference_location in role.locations
            or candidate.second_preference_location == "Any"
        ):
            self._score += self.scoring_weights["second_location"]

    @register_scoring_method
    def _score_clearance(self, candidate: C, role: R) -> None:
        self.disqualified = candidate.clearance < role.clearance

    @register_scoring_method
    def _check_nationality(self, candidate: C, role: R) -> None:
        """
        Nationality requirements come in three flavours: British national only, dual national, no restriction

        :return:
        """
        self.disqualified = role.nationality_requirement > candidate.british_national

    @register_scoring_method
    def _check_passport(self, candidate: C, role: R) -> None:
        self.disqualified = role.passport_requirement and not candidate.has_passport

    @register_scoring_method
    def _score_department(self, candidate: C, role: R) -> None:
        if role.department not in candidate.prior_departments:
            self._score += self.scoring_weights["department"]

    @register_scoring_method
    def _ethical_check(self, candidate: C, role: R) -> None:
        self.disqualified = (candidate.no_immigration and role.immigration_role) or (
            candidate.no_defence and role.defence_role
        )

    @register_scoring_method
    def _appropriate_for_year_group(self, candidate: C, role: R) -> None:
        self.disqualified = candidate.year_group not in role.suitable_year_groups

    @register_scoring_method
    def _stretch_check(self, candidate: C, role: R) -> None:
        if (not candidate.wants_private_office and role.private_office_role) or (
            not candidate.wants_line_management and role.line_management_role
        ):
            self.disqualified = True
        else:
            if candidate.wants_private_office and role.private_office_role:
                self._score += self.scoring_weights["stretch"]
            if candidate.wants_line_management and role.line_management_role:
                self._score += self.scoring_weights["stretch"]

    def _check_score(self) -> None:
        """
        The lowest acceptable score for a match. If the score is too low, set `self.disqualified` to `True`

        :return:
        """
        if self.score < 20:
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
    @register_scoring_method
    def _score_skill(self, candidate: C, role: R) -> None:
        if role.secondary_focus == candidate.last_role_secondary_skill:
            self._score -= 5
        bonus = self.scoring_weights["skill"]
        for skill in (candidate.primary_skill, candidate.secondary_skill):
            for focus in (role.skill_focus, role.secondary_focus):
                if skill == focus:
                    self._score += bonus
                bonus -= 5
