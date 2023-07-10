from typing import Literal

from fast_stream_22.matching import Role, Candidate
from fast_stream_22.specialism.pair import register_scoring_method, BasePair

Level = Literal["P", "A", "N"]
Skills = Literal[
    "Broad Thinking",
    "Building and Applying Knowledge",
    "Communicating Science & Engineering for Government",
    "Technical Oversight and Management",
    "Developing the GSE community",
]


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
            "Broad Thinking": broad_thinking,
            "Building and Applying Knowledge": building_applying,
            "Communicating Science & Engineering for Government": communicating,
            "Technical Oversight and Management": oversight,
            "Developing the GSE community": developing,
        }


class SefsPair(BasePair):
    @register_scoring_method
    def _score_skill(self) -> None:
        """
        This method scores the specifics of the SEFS specialism

        :param candidate:
        :param role:
        :return:
        """
        skills_valence_map: dict[str, float] = {
            self.candidate.primary_skill: 1.0,
            self.candidate.secondary_skill: 0.8,
        }
        if not self.candidate.year_group == 1:
            skill_score = 0
            for skill, valence in skills_valence_map.items():
                if self.role.skills[skill] == "P":
                    skill_score += int(self.scoring_weights["skill"] * valence)
            if self.role.skills[self.candidate.not_required_skill] == "P":
                skill_score = int(skill_score / 2)
            if skill_score == 0:
                self.disqualified = True
            else:
                self._score += skill_score
