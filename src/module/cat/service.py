# -*- coding: utf-8 -*-
from typing import Type

from src.common.services import CommonService
from src.module.models import Cat


class CatService(CommonService):
    def __init__(self, model: Type[Cat]):
        self.Model = model
        super().__init__(model)
