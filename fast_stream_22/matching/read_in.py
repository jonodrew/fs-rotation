from __future__ import annotations

import csv
import functools
from typing import Sequence, Type, TypeVar

from fast_stream_22.matching.models import Candidate, Role, BaseClass


@functools.lru_cache
def read_candidates(path_to_csv: str = "./candidates.csv") -> Sequence[Candidate]:
    return _read_and_create_objects(path_to_csv, Candidate)


@functools.lru_cache
def read_roles(path_to_csv: str = "./roles.csv") -> Sequence[Role]:
    return _read_and_create_objects(path_to_csv, Role)


MatchObject = TypeVar("MatchObject", bound=BaseClass)


def _read_and_create_objects(
    filepath: str, model: Type[MatchObject]
) -> list[MatchObject]:
    with open(filepath) as file:
        return [model(**line) for line in csv.DictReader(file)]
