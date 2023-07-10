from unittest.mock import patch

from fast_stream_22.matching.match import conduct_matching


def test_conduct_matching():
    with patch("fast_stream_22.specialism.pair.Pair._check_score"):
        conduct_matching(
            "CML/2022-11-21 - CML - BIDS.csv",
            "CML/2022-11-21 - CML - roles.csv",
            "CML/2022-11-21 - CML - candidates.csv",
            senior_first=True,
            specialism=None,
            iterations=1,
        )
        assert True
