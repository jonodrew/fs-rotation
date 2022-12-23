from unittest.mock import MagicMock, patch, PropertyMock

from fast_stream_22.matching.match import Process, Bid
from fast_stream_22.matching.models import Candidate, Role


class TestProcess:
    def test_when_bids_full_no_more_roles_from_that_department(self):
        bids = [Bid(1, "CO", 5)]
        candidates = [
            MagicMock(
                spec=Candidate, **{"uid": f"c-{i}", "paired": False, "year_group": 1}
            )
            for i in range(10)
        ]
        roles = [
            MagicMock(
                spec=Role,
                **{
                    "uid": f"r-{i}",
                    "paired": False,
                    "suitable_year_groups": {1},
                    "priority_role": 3,
                    "department": "CO",
                },
            )
            for i in range(15)
        ]
        with patch(
            "fast_stream_22.matching.match.Process.all_roles", new_callable=PropertyMock
        ) as mock_get_roles, patch(
            "fast_stream_22.matching.match.Process.pair_off"
        ) as mock_pairs:
            mock_pairs.return_value = [(f"c-{i}", f"r-{i}") for i in range(5)]
            p = Process(candidates, roles, bids)
            p.max_rounds = 1
            mock_get_roles.return_value = roles
            assert p.match_cohort(1)
            assert p.bids[0].count == 5

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
