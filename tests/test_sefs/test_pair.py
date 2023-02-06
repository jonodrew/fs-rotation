from unittest.mock import Mock

from fast_stream_22.matching.SEFS.models import SefsPair, Pair


def test_when_pair_created_scoring_method_added_to_parent_class():
    p = SefsPair(Mock(), Mock())
    assert SefsPair._score_skill.__name__ in p.scoring_method_names
    assert Pair._score_location.__name__ in p.scoring_method_names
