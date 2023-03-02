import random
import uuid
from typing import Literal, TypeVar

import pytest

from fast_stream_22.matching.models import Role, Candidate, BaseClass

T = TypeVar("T", bound=BaseClass)


@pytest.fixture
def candidate_factory():
    def _candidate_factory(kwargs):
        return object_factory("candidate", kwargs)

    return _candidate_factory


@pytest.fixture
def role_factory():
    def _role_factory(kwargs):
        return object_factory("role", kwargs)

    return _role_factory


def object_factory(object_type: Literal["candidate", "role"], kwargs) -> T:
    return {"candidate": Candidate, "role": Role}[object_type](**kwargs)  # type: ignore


@pytest.fixture
def random_candidates(random_candidate_dict):
    return [Candidate(**random_candidate_dict()) for i in range(50)]


@pytest.fixture
def random_candidate_dict():
    def _random_candidate():
        candidate = {
            "uuid": f"C-{uuid.uuid4()}",
            "clearance_held": random.choice(["SC", "DV"]),
            "year_group": random.choice([i for i in range(1, 4)]),
            "can_relocate": True,
            "first_location_preference": random.choice(locations),
            "second_location_preference": random.choice([*locations, None]),
            "wants_line_management": True,
            "wants_private_office": True,
            "no_defence": False,
            "no_immigration": False,
            "preferred_office_attendance": "",
            "primary_skills_seeking": "Operational",
            "secondary_skills_seeking": "Digital",
            "british_national": "British National",
            "has_passport": True,
            "last_role_main_skill": "Policy",
            "last_role_secondary_skill": "Corporate",
        }
        candidate["prior_departments"] = ",".join(
            random.sample(departments, k=candidate["year_group"] - 1)
        )
        c = {key: str(value) for key, value in candidate.items()}
        return c

    return _random_candidate


@pytest.fixture
def random_role_dict():
    def _random_role():
        role = {
            "uuid": f"R-{uuid.uuid4()}",
            "clearance_required": "SC",
            "nationality_requirement": "British National",
            "passport_requirement": bool(random.getrandbits(1)),
            "location": random.choice(locations),
            "department": random.choice(departments),
            "priority_role": random.choice(["High", "Medium", "Low"]),
            "suitable_for_year_group": ",".join(
                map(
                    str, random.sample([i for i in range(1, 4)], k=random.randint(1, 3))
                )
            ),
            "private_office_role": False,
            "line_management_role": False,
            "office_arrangement": "",
            "travel_requirements": "Outside Region",
            "defence_role": False,
            "immigration_role": False,
            "skill_focus": random.choice(skills),
            "secondary_focus": random.choice(skills),
        }
        return {key: str(value) for key, value in role.items()}

    return _random_role


@pytest.fixture
def random_roles(random_role_dict):
    return [Role(**random_role_dict()) for i in range(75)]


departments = ["DWP", "HO", "MOJ", "MOD", "HMRC", "CO", "BEIS"]
locations = [
    "London",
    "South East",
    "South West",
    "North East",
    "North West",
    "Midlands",
    "Manchester",
    "Glasgow",
]
skills = ["Operations", "Finance", "Policy", "Digital"]
