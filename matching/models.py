from enum import Enum
from typing import Literal, Sequence

SkillLevel = Literal[0, 1, 2, 3, 4, 5]
Skills = dict[str, SkillLevel]

StrBool = Literal["true", "false"]


class Clearance(Enum):
    BPSS = 1
    CTC = 2
    SC = 3
    DV = 4


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
        id_string: str,
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
        skills_sought: str,
    ):
        super().__init__(id_string, clearance_held)
        self.can_relocate = bool(can_relocate)
        self.first_preference_location = first_location_preference
        self.second_preference_location = second_location_preference
        self.year_group = int(year_group)
        self.prior_departments = set(prior_departments.split(","))
        self.wants_line_management = bool(wants_line_management)
        self.wants_private_office = bool(wants_private_office)
        self.no_defence = bool(no_defence)
        self.no_immigration = bool(no_immigration)
        self.preferred_office_attendance = preferred_office_attendance
        self.skills_sought: Sequence[str] = skills_sought.split(",")


class Role(BaseClass):
    def __init__(
        self,
        name: str,
        clearance_required: str,
        nationality_requirement: StrBool,
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
    ):
        super().__init__(
            name,
            clearance_required,
        )
        self.nationality_requirement = bool(nationality_requirement)
        self.passport_requirement = bool(passport_requirement)
        self.location = location
        self.department = department
        self.priority_role = bool(priority_role)
        self.suitable_years_groups = {
            int(year) for year in suitable_for_year_group.split(",")
        }
        self.private_office_role = bool(private_office_role)
        self.line_management_role = bool(line_management_role)
        self.office_arrangements = office_arrangement
        self.travel_requirements = travel_requirements
        self.defence_role = bool(defence_role)
        self.immigration_role = bool(immigration_role)
        self.skill_focus = skill_focus

    @property
    def clearance_required(self) -> Clearance:
        return self.clearance


class Pair:
    def __init__(self, c: Candidate, r: Role):
        self.candidate = c
        self.role = r
        self.score: int = 0

    def score_pair(self):
        pass
