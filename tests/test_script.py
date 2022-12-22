from fast_stream_22.scripts.process_pairs import conduct_matching


def test_script():
    assert conduct_matching("../bids.csv", "../roles.csv", "../candidates.csv")
