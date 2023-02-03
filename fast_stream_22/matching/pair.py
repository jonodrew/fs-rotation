from typing import Callable, TypeVar

from fast_stream_22.matching.models import Candidate, Role


P = TypeVar("P", bound="Pair")


class RuleSet(set):
    def __call__(self, rule: Callable[[P], None]) -> Callable[[P], None]:
        """
        This allows an instance of this class to decorate a scoring rule. It then registers it on the class, allowing us
        to collect all the scoring rules together and then call them one-by-one

        :param rule: a method that takes a `Pair` instance and returns None
        :return: the function
        """
        self.add(rule)
        return rule


C = TypeVar("C", bound=Candidate)
R = TypeVar("R", bound=Role)


class Pair:
    scoring_weights: dict[str, int] = {
        "first_location": 10,
        "second_location": 5,
        "department": 10,
        "skill": 20,
        "stretch": 10,
    }
    scoring_methods = RuleSet()

    def __init__(self, candidate: C, role: R):
        self.candidate = candidate
        self.role = role
        self._score: int = 0
        self._disqualified = False

    def score_pair(self) -> int:
        for method in self.scoring_methods:
            method(self)
        self._check_score()
        return self._score

    @scoring_methods
    def _check_location(self):
        if not self.candidate.can_relocate:
            self._disqualified = not (
                self.role.from_anywhere()
                or self.candidate.first_preference_location in self.role.locations
                or self.candidate.second_preference_location in self.role.locations
            )

    @scoring_methods
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

    @scoring_methods
    def _score_clearance(self):
        self.disqualified = self.candidate.clearance < self.role.clearance

    @scoring_methods
    def _check_nationality(self):
        """
        Nationality requirements come in three flavours: British national only, dual national, no restriction

        :return:
        """
        self.disqualified = (
            self.role.nationality_requirement > self.candidate.british_national
        )

    @scoring_methods
    def _check_passport(self):
        self.disqualified = (
            self.role.passport_requirement and not self.candidate.has_passport
        )

    @scoring_methods
    def _score_department(self):
        if self.role.department not in self.candidate.prior_departments:
            self._score += self.scoring_weights["department"]

    @scoring_methods
    def _ethical_check(self):
        self.disqualified = (
            self.candidate.no_immigration and self.role.immigration_role
        ) or (self.candidate.no_defence and self.role.defence_role)

    @scoring_methods
    def _appropriate_for_year_group(self):
        self.disqualified = (
            self.candidate.year_group not in self.role.suitable_year_groups
        )

    @scoring_methods
    def _score_skill(self) -> None:
        if self.role.secondary_focus == self.candidate.last_role_secondary_skill:
            self._score -= 5
        bonus = self.scoring_weights["skill"]
        for skill in (self.candidate.primary_skill, self.candidate.secondary_skill):
            for focus in (self.role.skill_focus, self.role.secondary_focus):
                if skill == focus:
                    self._score += bonus
                bonus -= 5

    @scoring_methods
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
