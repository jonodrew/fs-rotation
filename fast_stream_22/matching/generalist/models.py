import functools
from enum import IntEnum

from fast_stream_22.matching import BasePair, Candidate, Role
from fast_stream_22.matching.pair import register_scoring_method


class Travel(IntEnum):
    NO_TRAVEL = 1
    LOCAL = 2
    NATIONAL = 3

    @classmethod
    @functools.lru_cache
    def factory(cls, travel: str):
        mapping = {
            "I can travel nationally": cls.NATIONAL,
            "I can travel locally, within the same region": cls.LOCAL,
            "I'm unable to travel regularly": cls.NO_TRAVEL,
            "Outside Region": cls.NATIONAL,
            "Within Region": cls.LOCAL,
            "None": cls.NO_TRAVEL,
        }
        return mapping[travel]


class GeneralistCandidate(Candidate):
    def __init__(
        self,
        primary_anchor_seeking: str,
        secondary_anchor_seeking: str,
        dept_pref_1: str,
        dept_pref_2: str,
        dept_pref_3: str,
        dept_pref_4: str,
        dept_pref_5: str,
        travel_requirements: str,
        accessibility: str = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.primary_anchor = primary_anchor_seeking
        self.secondary_anchor = secondary_anchor_seeking
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
        self.travel_requirements: Travel = Travel.factory(travel_requirements)

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
    def __init__(self, accessibility: str, anchor: str, **kwargs):
        self.secondment = False
        if "6m" in kwargs["suitable_for_year_group"]:
            self.secondment = True
            kwargs["suitable_for_year_group"] = kwargs[
                "suitable_for_year_group"
            ].replace("6m", "2")
        super().__init__(**kwargs)
        self.accessibility = accessibility
        self.anchor = anchor


class GeneralistPair(BasePair):
    @register_scoring_method
    def _appropriate_for_year_group(
        self, candidate: GeneralistCandidate, role: GeneralistRole
    ) -> None:
        self.disqualified = candidate.secondment ^ role.secondment
        super()._appropriate_for_year_group(candidate, role)
