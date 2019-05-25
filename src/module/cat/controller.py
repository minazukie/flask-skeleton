# -*- coding: utf-8 -*-
from flask_restful import Resource

from src.module.cat.dto import NewCatDTO, UpdateCatDTO
from src.module.cat.manager import CatManager
from src.module.cat.parser import CatListParser
from src.module.parsers import CommonRequestParser


class CatListController(Resource):
    def __init__(self, manager: CatManager, parser: CatListParser, **kwargs):
        self._manager = manager
        self._parser = parser
        super().__init__(**kwargs)

    def get(self) -> dict:
        where_args, page_args = self._parser.split_args()
        return self._manager.find("cats", where_args, page_args)

    def post(self) -> dict:
        payload = NewCatDTO.from_dict(self._parser.json())
        return self._manager.new(payload)


class CatController(Resource):
    def __init__(self, manager: CatManager, parser: CommonRequestParser, **kwargs):
        self._manager = manager
        self._parser = parser
        super().__init__(**kwargs)

    def get(self, cat_id: str) -> dict:
        return self._manager.get(cat_id)

    def put(self, cat_id: str) -> dict:
        payload = UpdateCatDTO.from_dict(self._parser.json())
        return self._manager.update(cat_id, payload)

    def delete(self, cat_id: str) -> dict:
        return self._manager.remove(cat_id)
