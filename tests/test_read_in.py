from fast_stream_22.specialism.models import Candidate


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
            "Policy",
            "Digital",
            "British National",
            "true",
            "Ops",
            "Digital",
        ]
        candidate = Candidate(*c_data_row)
        assert candidate
