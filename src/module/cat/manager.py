# -*- coding: utf-8 -*-
from src.module.cat.dto import NewCatDTO, UpdateCatDTO
from src.module.cat.service import CatService


class CatManager:
    def __init__(self, service: CatService):
        self._service = service

    def new(self, data: NewCatDTO):
        return self._service.create(data.to_dict())

    def find(self, name: str, where: dict, page_args: dict):
        return self._service.list(name, where, page_args)

    def get(self, cat_id: str):
        return self._service.get_resource_by_id(cat_id)

    def update(self, cat_id: str, data: UpdateCatDTO):
        return self._service.update(cat_id, data.to_dict())

    def remove(self, cat_id: str):
        return self._service.remove(cat_id)
