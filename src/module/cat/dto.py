# -*- coding: utf-8 -*-
from dataclasses import dataclass
from dataclasses_jsonschema import JsonSchemaMixin


@dataclass
class NewCatDTO(JsonSchemaMixin):
    name: str
    age: int
    gender: int
    birthday: int


@dataclass
class UpdateCatDTO(JsonSchemaMixin):
    name: str
