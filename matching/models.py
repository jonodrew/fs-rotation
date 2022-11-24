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
        clearance_required: Clearance,
        location: str,
        skill_increase: Skills,
        owner_email_address: str,
    ):
        super().__init__(
            name, clearance_required, location, skill_increase, owner_email_address
        )

    @property
    def location(self) -> str:
        return self._location

    @property
    def clearance_required(self) -> Clearance:
        return self._clearance

    @property
    def skill_growth(self) -> Skills:
        return self._skills

    @property
    def role_owner_email(self):
        return self._email
