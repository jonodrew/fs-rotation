import random
import uuid

import pytest


@pytest.fixture
def candidate_data():
    return [random_candidate() for i in range(50)]


def random_candidate():
    candidate = {
        "id": f"C-{uuid.uuid4()}",
        "clearance_held": random.choice(["SC", "DV"]),
        "year_group": random.choice([i for i in range(1, 5)]),
        "can_relocate": bool(random.getrandbits(1)),
        "first_location_preference": random.choice(locations),
        "second_location_preference": random.choice([*locations, None]),
        "line_management": bool(random.getrandbits(1)),
        "private_office": bool(random.getrandbits(1)),
        "no_defence": bool(random.getrandbits(1)),
        "no_immigration": bool(random.getrandbits(1)),
        "preferred_office_attending": "",
    }
    candidate["prior_departments"] = ",".join(
        random.sample(departments, k=candidate["year_group"] - 1)
    )
    candidate["skills_seeking"] = ",".join(
        random.sample(skills, k=4 - (candidate["year_group"] - 1))
    )
    c = {key: str(value) for key, value in candidate.items()}
    return c


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
