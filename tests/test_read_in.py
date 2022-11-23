import random
import uuid

import pytest
from matching.models import Candidate

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


def random_candidate():
    candidate = {
        "id": f"C-{uuid.uuid4()}",
        "year_group": random.choice([i for i in range(1, 5)]),
        "relocation_restriction": bool(random.getrandbits(1)),
        "first_location_preference": random.choice(locations),
        "second_location_preference": random.choice([*locations, None]),
        "line_management": bool(random.getrandbits(1)),
        "private_office": bool(random.getrandbits(1)),
        "no_defence": bool(random.getrandbits(1)),
        "no_immigration": bool(random.getrandbits(1)),
    }
    candidate["prior_departments"] = ",".join(
        random.sample(departments, k=candidate["year_group"] - 1)
    )
    candidate["skills_seeking"] = ",".join(
        random.sample(skills, k=4 - (candidate["year_group"] - 1))
    )
    c = {
        key: str(value) if type(value) != list else value
        for key, value in candidate.items()
    }
    return c


@pytest.fixture
def candidate_data():
    return [random_candidate() for i in range(50)]


class TestInstantiation:
    def test_instantiate_candidate(self):
        c_data_row = [
            "C-1",
            "SC",
            "1",
            "",
            "London",
            "",
            "false",
            "false",
            "true",
            "false",
            "false",
            "",
            "Policy,Digital,Finance,Operational",
        ]
        candidate = Candidate(*c_data_row)
        assert candidate
