from __future__ import annotations
from typing import Literal
from matching.models import Candidate, Role


def score_skills(c: Candidate, r: Role) -> int | Literal[False]:
    """
    Calculate the score of the skills shortfall for this candidate, c
    """
    return sum(map(lambda name, level: _score_skill(c.current_skills[name], level), r.skill_growth.items()))


def _score_skill(c_skill: int, r_skill: int) -> int | Literal[False]:
    """
    Score a skill, weighting development opportunities. Note max score is 5
    :param c_skill: Candidate skill
    :param r_skill: role skill development
    :return: a value representing this opportunity
    """
    return (5 - c_skill) * r_skill


def score_location(c: Candidate, r: Role) -> int | Literal[False]:
    """
    Score the location of the proposed role, taking into account caring responsibilities
    :param c:
    :param r:
    :return:
    """
    if not c.can_relocate and c.current_location != r.location:
        return -1
    else:
        return int(r.location in c.preferred_locations)
