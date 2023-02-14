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
        self.secondment = False

    @property
    def year_group(self) -> int:
        return self._year_group

    @year_group.setter
    def year_group(self, year_group: str) -> None:
        if year_group.endswith("m"):
            self.secondment = True
            self._year_group = 2
        else:
            self._year_group = int(year_group)


class GeneralistRole(Role):
    ...
