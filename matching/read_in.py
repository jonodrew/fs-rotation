from __future__ import annotations

import csv
import functools
from typing import Sequence, Type, Union

from matching.models import Candidate, Role


@functools.lru_cache
def read_candidates() -> Sequence[Candidate]:
    return _read_and_create_objects("candidates.csv", Candidate)


@functools.lru_cache
def read_roles() -> Sequence[Role]:
    return _read_and_create_objects("roles.csv", Role)


def _correct_line(line_dict: dict[str, str]) -> dict[str, Union[int, str]]:
    fresh_dict = {}
    skills_dict = {}
    for key, value in line_dict.items():
        if key in {"Digital", "Operations", "Finance", "Policy"}:
            value = int(value)
            skills_dict[key] = int(value)
        else:
            fresh_dict[key] = value
    fresh_dict['skills'] = skills_dict
    return fresh_dict


def _read_and_create_objects(filepath: str, model: Type[Candidate] | Type[Role]) -> Sequence[Role | Candidate]:
    with open(filepath) as file:
        return [model(_correct_line(**line)) for line in csv.DictReader(file)]
