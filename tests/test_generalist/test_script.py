from fast_stream_22.scripts.process_pairs import conduct_matching


def test_can_match_generalists_with_csv_data():
    assert conduct_matching(
        bid_file="tests/test_generalist/test_bids.csv",
        role_file="tests/test_generalist/test_roles.csv",
        candidate_file="tests/test_generalist/test_candidates.csv",
        senior_first=False,
        specialism="generalist",
    )
