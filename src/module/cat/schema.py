# -*- coding: utf-8 -*-
import time
from dataclasses import dataclass, field
from typing import List

from dataclasses_jsonschema import JsonSchemaMixin


@dataclass
class Tag(JsonSchemaMixin):
    name: str
    level: int


@dataclass
class CatSchema(JsonSchemaMixin):
    name: str
    age: int
    gender: int   # 0: male 1: female 2: other
    birthday: int
    tags: List[Tag]
    state: str = 'active'
    created_at: int = field(default_factory=lambda: int(time.time()))
    updated_at: int = field(default_factory=lambda: int(time.time()))
