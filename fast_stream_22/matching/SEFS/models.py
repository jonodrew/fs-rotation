from typing import Literal

from fast_stream_22.matching import Pair, Role, Candidate

Level = Literal["P", "A", "N"]


class SefsCandidate(Candidate):
    def __init__(self, not_required: str, **kwargs):
        super().__init__(**kwargs)
        self.not_required_skill = not_required


class SefsRole(Role):
    def __init__(
        self,
        broad_thinking: Level,
        building_applying: Level,
        communicating: Level,
        oversight: Level,
        developing: Level,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.skills = {
            "broad_thinking": broad_thinking,
            "building_applying": building_applying,
            "communicating": communicating,
            "oversight": oversight,
            "developing": developing,
        }

    pass


class SefsPair(Pair):
    def __init__(self, candidate: SefsCandidate, role: SefsRole):
        super().__init__(candidate, role)

    @Pair.scoring_methods
    def _score_skill(self) -> None:
        pass
