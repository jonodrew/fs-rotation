from unittest.mock import MagicMock

import pytest

from fast_stream_22.matching.generalist.models import (
    GeneralistPair,
    GeneralistRole,
    GeneralistCandidate,
)


@pytest.mark.parametrize(
    ["candidate_secondment", "role_secondment", "expected"],
    [
        (True, False, True),
        (True, True, False),
        (False, False, False),
        (False, True, True),
    ],
)
def test_disqualify_secondment_flag(candidate_secondment, role_secondment, expected):
    p = GeneralistPair()
    c = MagicMock(GeneralistCandidate)
    c.secondment = candidate_secondment
    r = MagicMock(GeneralistRole)
    r.secondment = role_secondment
    c.year_group = 2
    r.suitable_year_groups = {2}
    assert not p.disqualified
    p._appropriate_for_year_group(c, r)
    assert p.disqualified is expected
