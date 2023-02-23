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
        (True, False, False),
        (True, True, False),
        (False, False, False),
        (False, True, False),
    ],
)
def test_disqualify_secondment_flag(candidate_secondment, role_secondment, expected):
    p = GeneralistPair()
    c = MagicMock(GeneralistCandidate)
    c.secondment = candidate_secondment
    r = MagicMock(GeneralistRole)
    r.secondment = role_secondment
    r.secondment_only = False
    c.year_group = 2
    r.suitable_year_groups = {2}
    assert not p.disqualified
    p._check_year_group(c, r)
    assert p.disqualified is expected
