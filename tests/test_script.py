from fast_stream_22.scripts.process_pairs import conduct_matching


def test_conduct_matching():
    conduct_matching(
        "CML/2022-11-21 - CML - BIDS.csv",
        "CML/2022-11-21 - CML - roles.csv",
        "CML/2022-11-21 - CML - candidates.csv",
        senior_first=True,
        specialism=None,
    )
    assert True
