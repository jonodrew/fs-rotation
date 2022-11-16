from __future__ import annotations
from matching.models import Candidate, Role


"""
Scoring functions should return -1 if the match should be disallowed. Otherwise, they return a nonnegative value
"""


def score_skills(c: Candidate, r: Role) -> int:
    """
    Calculate the score of the skills shortfall for this candidate, c
    """
    return sum(map(lambda name_level: _score_skill(c.current_skills[name_level[0]], name_level[1]), r.skill_growth.items()))


def _score_skill(c_skill: int, r_skill: int) -> int:
    """
    Score a skill, weighting development opportunities. Note max score is 5
    :param c_skill: Candidate skill
    :param r_skill: role skill development
    :return: a value representing this opportunity
    """
    return (5 - c_skill) * r_skill


def score_location(c: Candidate, r: Role) -> int:
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


def score_clearance(c: Candidate, r: Role) -> int:
    return 1 if c.clearance.value >= r.clearance_required.value else -1

