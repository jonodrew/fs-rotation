from enum import IntEnum
from typing import Literal
import json

SkillLevel = Literal[0, 1, 2, 3, 4, 5]
Skills = dict[str, SkillLevel]

StrBool = Literal["true", "false"]


class Clearance(IntEnum):
    BPSS = 1
    CTC = 2
    SC = 3
    DV = 4


class Nationality(IntEnum):
    REST_OF_WORLD = 1
    DUAL_NATIONAL = 2
    BRITISH_NATIONAL = 3


class NationalityRequirement(IntEnum):
    NO_RESTRICTION = 1
    DUAL_NATIONAL = 2
    BRITISH_NATIONAL = 3


class BaseClass:
    def __init__(self, uid: str, clearance: str):
        self.uid = uid
        self._clearance = Clearance[clearance]

    @property
    def clearance(self) -> Clearance:
        return self._clearance


class Candidate(BaseClass):
    def __init__(
        self,
        uuid: str,
        clearance_held: str,
        year_group: str,
        prior_departments: str,
        first_location_preference: str,
        second_location_preference: str,
        can_relocate: StrBool,
        wants_line_management: StrBool,
        wants_private_office: StrBool,
        no_defence: StrBool,
        no_immigration: StrBool,
        preferred_office_attendance: str,
        primary_skills_seeking: str,
        secondary_skills_seeking: str,
        british_national: str,
        has_passport: StrBool,
    ):
        super().__init__(uuid, clearance_held)
        self.can_relocate = json.loads(can_relocate.lower())
        self.first_preference_location = first_location_preference
        self.second_preference_location = second_location_preference
        self.year_group = int(year_group)
        self.prior_departments = set(prior_departments.split(","))
        self.wants_line_management = json.loads(wants_line_management.lower())
        self.wants_private_office = json.loads(wants_private_office.lower())
        self.no_defence = json.loads(no_defence.lower())
        self.no_immigration = json.loads(no_immigration.lower())
        self.preferred_office_attendance = preferred_office_attendance
        self.primary_skill = primary_skills_seeking
        self.secondary_skill = secondary_skills_seeking
        self.british_national = Nationality[british_national.replace(" ", "_").upper()]
        self.has_passport = json.loads(has_passport.lower())


class Role(BaseClass):
    def __init__(
        self,
        uuid: str,
        clearance_required: str,
        nationality_requirement: str,
        passport_requirement: StrBool,
        location: str,
        department: str,
        priority_role: StrBool,
        suitable_for_year_group: str,
        private_office_role: StrBool,
        line_management_role: StrBool,
        office_arrangement: str,
        travel_requirements: str,
        defence_role: StrBool,
        immigration_role: StrBool,
        skill_focus: str,
        secondary_focus: str,
    ):
        super().__init__(
            uuid,
            clearance_required,
        )
        self.nationality_requirement = NationalityRequirement[
            nationality_requirement.replace(" ", "_").upper()
        ]
        self.passport_requirement = json.loads(passport_requirement.lower())
        self.location = location
        self.department = department
        self.priority_role = json.loads(priority_role.lower())
        self.suitable_year_groups = {
            int(year) for year in suitable_for_year_group.split(",")
        }
        self.private_office_role = json.loads(private_office_role.lower())
        self.line_management_role = json.loads(line_management_role.lower())
        self.office_arrangements = office_arrangement
        self.travel_requirements = travel_requirements
        self.defence_role = json.loads(defence_role.lower())
        self.immigration_role = json.loads(immigration_role.lower())
        self.skill_focus = skill_focus
        self.secondary_focus = secondary_focus

    @property
    def clearance_required(self) -> Clearance:
        return self.clearance


class Pair:
    scoring_weights: dict[str, int] = {
        "first_location": 10,
        "second_location": 5,
        "department": 10,
        "skill": 20,
        "stretch": 10,
        "priority": 10,
    }

    def __init__(self, c: Candidate, r: Role):
        self.candidate = c
        self.role = r
        self._score: int = 0
        self._disqualified = False
        if self.role.priority_role:
            self._score += self.scoring_weights["priority"]

    def score_pair(self) -> int:
        self._score_location()
        self._score_clearance()
        self._score_department()
        self._ethical_check()
        self._appropriate_for_year_group()
        self._score_skill()
        self._stretch_check()
        self._check_nationality()
        self._check_travel()
        return self._score

    def _score_location(self):
        if (
            self.role.location != self.candidate.first_preference_location
            and not self.candidate.can_relocate
        ):
            self.disqualified = True
        elif (
            self.role.location == self.candidate.first_preference_location
            or self.candidate.first_preference_location == "Any"
        ):
            self._score += self.scoring_weights["first_location"]
        elif (
            self.role.location == self.candidate.second_preference_location
            or self.candidate.second_preference_location == "Any"
        ):
            self._score += self.scoring_weights["second_location"]

    def _score_clearance(self):
        self.disqualified = self.candidate.clearance < self.role.clearance

    def _check_nationality(self):
        """
        Nationality requirements come in three flavours: British national only, dual national, no restriction

        :return:
        """
        self.disqualified = (
            self.role.nationality_requirement > self.candidate.british_national
        )

    def _check_travel(self):
        self.disqualified = (
            self.role.travel_requirements and not self.candidate.has_passport
        )

    def _score_department(self):
        if self.role.department not in self.candidate.prior_departments:
            self._score += self.scoring_weights["department"]

    def _ethical_check(self):
        self.disqualified = (
            self.candidate.no_immigration and self.role.immigration_role
        ) or (self.candidate.no_defence and self.role.defence_role)

    def _appropriate_for_year_group(self):
        self.disqualified = (
            self.candidate.year_group not in self.role.suitable_year_groups
        )

    def _score_skill(self):
        bonus = self.scoring_weights["skill"]
        for skill in (self.candidate.primary_skill, self.candidate.secondary_skill):
            for focus in (self.role.skill_focus, self.role.secondary_focus):
                if skill == focus:
                    self._score += bonus
                bonus -= 5

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
