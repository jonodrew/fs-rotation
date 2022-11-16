from __future__ import annotations

import csv
import functools
from typing import Sequence, Type

from matching.models import Candidate, Role


@functools.lru_cache
def read_candidates() -> Sequence[Candidate]:
    return _read_and_create_objects("candidates.csv", Candidate)


@functools.lru_cache
def read_roles() -> Sequence[Role]:
    return _read_and_create_objects("roles.csv", Role)


def _read_and_create_objects(filepath: str, model: Type[Candidate] | Type[Role]) -> Sequence[Role | Candidate]:
    with open(filepath) as file:
        return [model(**line) for line in csv.DictReader(file)]
