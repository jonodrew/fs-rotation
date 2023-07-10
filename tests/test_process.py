from unittest.mock import MagicMock

from fast_stream_22.matching.match import Process, Bid
from fast_stream_22.specialism.models import Candidate


class TestProcess:
    def test_all_roles_property_sorts_correctly(self, random_roles):
        p = Process(
            [
                MagicMock(
                    spec=Candidate,
                    **{"uid": f"c-{i}", "paired": False, "year_group": 1},
                )
                for i in range(10)
            ],
            random_roles,
            bids=[Bid(1, "CO", 5)],
        )
        all_roles = p.all_roles
        first = all_roles[0]
        last = all_roles[-1]
        assert first.priority_role.value > last.priority_role.value
