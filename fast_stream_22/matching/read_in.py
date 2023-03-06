from __future__ import annotations

import csv
import functools
from typing import Type, TypeVar, Optional, MutableSequence

from fast_stream_22.matching.SEFS.models import SefsRole, SefsCandidate
from fast_stream_22.matching.generalist.models import (
    GeneralistCandidate,
    GeneralistRole,
)
from fast_stream_22.matching.models import Candidate, Role, BaseClass


@functools.lru_cache
def read_candidates(
    path_to_csv: str = "./candidates.csv", specialism: str = None
) -> MutableSequence[Candidate]:
    specialisms = {
        None: Candidate,
        "SEFS": SefsCandidate,
        "generalist": GeneralistCandidate,
    }
    return _read_and_create_objects(path_to_csv, specialisms[specialism])


@functools.lru_cache
def read_roles(
    path_to_csv: str = "./roles.csv", specialism: Optional[str] = None
) -> MutableSequence[Role]:
    specialisms = {"SEFS": SefsRole, None: Role, "generalist": GeneralistRole}
    return _read_and_create_objects(path_to_csv, specialisms[specialism])


MatchObject = TypeVar("MatchObject", bound=BaseClass)


def _read_and_create_objects(
    filepath: str, model: Type[MatchObject]
) -> list[MatchObject]:
    objs = []
    with open(filepath) as file:
        for line in csv.DictReader(file):
            line = {k: v.strip() for k, v in line.items()}
            objs.append(model(**line))
    return objs
