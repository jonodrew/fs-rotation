from fast_stream_22.matching import BasePair, Candidate, Role


class GeneralistPair(BasePair):
    ...


class GeneralistCandidate(Candidate):
    def __init__(
        self,
        primary_anchor: str,
        secondary_anchor: str,
        dept_pref_1: str,
        dept_pref_2: str,
        dept_pref_3: str,
        dept_pref_4: str,
        dept_pref_5: str,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.primary_anchor = primary_anchor
        self.secondary_anchor = secondary_anchor
        self.dept_prefs = [
            self._stringify_department(dept)
            for dept in [
                dept_pref_1,
                dept_pref_2,
                dept_pref_3,
                dept_pref_4,
                dept_pref_5,
            ]
        ]


class GeneralistRole(Role):
    ...
