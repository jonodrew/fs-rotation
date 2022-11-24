import random
import uuid

import pytest

from matching.models import Role


@pytest.fixture
def candidate_data(random_candidate):
    return [random_candidate() for i in range(50)]


@pytest.fixture
def random_candidate_dict():
    def _random_candidate():
        candidate = {
            "uuid": f"C-{uuid.uuid4()}",
            "clearance_held": random.choice(["SC", "DV"]),
            "year_group": random.choice([i for i in range(1, 5)]),
            "can_relocate": bool(random.getrandbits(1)),
            "first_location_preference": random.choice(locations),
            "second_location_preference": random.choice([*locations, None]),
            "wants_line_management": bool(random.getrandbits(1)),
            "wants_private_office": bool(random.getrandbits(1)),
            "no_defence": bool(random.getrandbits(1)),
            "no_immigration": bool(random.getrandbits(1)),
            "preferred_office_attendance": "",
        }
        candidate["prior_departments"] = ",".join(
            random.sample(departments, k=candidate["year_group"] - 1)
        )
        candidate["skills_seeking"] = ",".join(
            random.sample(skills, k=4 - (candidate["year_group"] - 1))
        )
        c = {key: str(value) for key, value in candidate.items()}
        return c

    return _random_candidate


@pytest.fixture
def random_role_dict():
    def _random_role():
        role = {
            "uuid": f"R-{uuid.uuid4()}",
            "clearance_required": random.choice(["DV", "SC"]),
            "nationality_requirement": bool(random.getrandbits(1)),
            "passport_requirement": bool(random.getrandbits(1)),
            "location": random.choice(locations),
            "department": random.choice(departments),
            "priority_role": bool(random.getrandbits(1)),
            "suitable_for_year_group": ",".join(
                map(
                    str, random.sample([i for i in range(1, 5)], k=random.randint(1, 4))
                )
            ),
            "private_office_role": bool(random.getrandbits(1)),
            "line_management_role": bool(random.getrandbits(1)),
            "office_arrangement": "",
            "travel_requirements": "",
            "defence_role": bool(random.getrandbits(1)),
            "immigration_role": bool(random.getrandbits(1)),
            "skill_focus": random.choice(skills),
        }
        return {key: str(value) for key, value in role.items()}

    return _random_role


@pytest.fixture
def random_roles(random_role):
    return [Role(**random_role()) for i in range(75)]


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
