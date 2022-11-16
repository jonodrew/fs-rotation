from enum import Enum
from typing import Literal, Collection

SkillLevel = Literal[0, 1, 2, 3, 4, 5]
Skills = dict[str, SkillLevel]


class Clearance(Enum):
    BPSS = 1
    CTC = 2
    SC = 3
    DV = 4


class BaseClass:
    def __init__(self, name: str, clearance: Clearance, location: str, skills: Skills, email_address: str):
        self.name = name
        self._clearance = clearance
        self._location = location
        self._skills = skills
        self._email = email_address


class Candidate(BaseClass):
    def __init__(self, name: str, clearance_held: Clearance, current_location: str, current_skills: Skills,
                 email_address: str, can_relocate: bool, preferred_locations: Collection[str]):
        super().__init__(name, clearance_held, current_location, current_skills, email_address)
        self.can_relocate = can_relocate
        self.preferred_locations = preferred_locations

    @property
    def clearance(self) -> Clearance:
        return self._clearance

    @property
    def current_location(self) -> str:
        return self._location

    @property
    def current_skills(self) -> Skills:
        return self._skills

    @property
    def email_address(self) -> str:
        return self._email


class Role(BaseClass):
    def __init__(self, name: str, clearance_required: Clearance, location: str, skill_increase: Skills,
                 owner_email_address: str):
        super().__init__(name, clearance_required, location, skill_increase, owner_email_address)

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
