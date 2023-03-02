import functools
from enum import IntEnum
from typing import Literal, Optional, Self  # type: ignore
import json

SkillLevel = Literal[0, 1, 2, 3, 4, 5]
Skills = dict[str, SkillLevel]

StrBool = Literal["true", "false"]


class Priority(IntEnum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


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
    departments: set[str] = set()

    def __init__(self, uid: str, clearance: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uid = uid
        self._clearance = Clearance[clearance]
        self.paired = False

    @classmethod
    def _stringify_department(cls, dept: str) -> str:
        dept = dept.lower().strip()
        cls.departments.add(dept)
        return dept

    @property
    def clearance(self) -> Clearance:
        return self._clearance

    def mark_paired(self):
        self.paired = True

    def __repr__(self):
        return self.uid


class Candidate(BaseClass):
    departments: set[str] = set()

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
        last_role_main_skill: Optional[str] = None,
        last_role_secondary_skill: Optional[str] = None,
    ):
        super().__init__(uuid, clearance_held)
        self.can_relocate = json.loads(can_relocate.lower())
        self.first_preference_location = first_location_preference
        self.second_preference_location = second_location_preference
        self.year_group = Cohort.factory(year_group)
        self.prior_departments = set(
            map(self._stringify_department, prior_departments.split(","))
        )
        self.wants_line_management = json.loads(wants_line_management.lower())
        self.wants_private_office = json.loads(wants_private_office.lower())
        self.no_defence = json.loads(no_defence.lower())
        self.no_immigration = json.loads(no_immigration.lower())
        self.preferred_office_attendance = preferred_office_attendance
        self.primary_skill = primary_skills_seeking
        self.secondary_skill = secondary_skills_seeking
        self.british_national = Nationality[british_national.replace(" ", "_").upper()]
        self.has_passport = json.loads(has_passport.lower())
        self.last_role_main_skill = last_role_main_skill
        self.last_role_secondary_skill = last_role_secondary_skill


class Role(BaseClass):
    departments: set[str] = set()

    def __init__(
        self,
        uuid: str,
        clearance_required: str,
        nationality_requirement: str,
        passport_requirement: StrBool,
        location: str,
        department: str,
        priority_role: str,
        suitable_for_year_group: str,
        private_office_role: StrBool,
        line_management_role: StrBool,
        office_arrangement: str,
        defence_role: StrBool,
        travel_requirements: str,
        immigration_role: StrBool,
        skill_focus: str,
        secondary_focus: str,
    ):
        super().__init__(
            uuid,
            clearance_required,
        )
        self._nationality_requirement = NationalityRequirement[
            nationality_requirement.replace(" ", "_").upper()
        ]
        self.passport_requirement = json.loads(passport_requirement.lower())
        self.locations = {loc.strip() for loc in location.split(",")}
        self.department = self._stringify_department(department)
        self.priority_role = Priority[priority_role.upper()]
        self.suitable_year_groups: set[Cohort] = {
            Cohort.factory(year) for year in suitable_for_year_group.split(",")
        }
        self.private_office_role = json.loads(private_office_role.lower())
        self.line_management_role = json.loads(line_management_role.lower())
        self.office_arrangements = office_arrangement
        self.travel_requirements = Travel.factory(travel_requirements)
        self.defence_role = json.loads(defence_role.lower())
        self.immigration_role = json.loads(immigration_role.lower())
        self.skill_focus = skill_focus
        self.secondary_focus = secondary_focus
        self.no_match: bool = False

    @property
    def clearance_required(self) -> Clearance:
        return self.clearance

    def from_anywhere(self) -> bool:
        return not {"Available Nationally", "Remote"}.isdisjoint(self.locations)

    @property
    def nationality_requirement(self) -> NationalityRequirement:
        if self.clearance_required == Clearance.BPSS:
            return NationalityRequirement.NO_RESTRICTION
        else:
            return self._nationality_requirement


class Travel(IntEnum):
    NO_TRAVEL = 1
    LOCAL = 2
    NATIONAL = 3

    @classmethod
    @functools.lru_cache
    def factory(cls, travel: str) -> "Travel":
        mapping = {
            "I can travel nationally": cls.NATIONAL,
            "I can travel locally, within the same region": cls.LOCAL,
            "I'm unable to travel regularly": cls.NO_TRAVEL,
            "Outside Region": cls.NATIONAL,
            "Within Region": cls.LOCAL,
            "None": cls.NO_TRAVEL,
        }
        return mapping[travel]


class Cohort(IntEnum):
    One = 1
    Two = 2
    Secondment = 3
    Three = 4

    @classmethod
    def factory(cls, cohort_str) -> Self:  # type: ignore
        mapping = {"1": cls.One, "2": cls.Two, "3": cls.Three, "6m": cls.Secondment}
        return mapping[cohort_str]
