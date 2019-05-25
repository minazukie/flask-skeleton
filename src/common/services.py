# -*- coding: utf-8 -*-
from typing import Union

from mongoengine.errors import DoesNotExist

from src.common.exceptions import ResourceNotExistError
from src.module.parsers import paginated_wrapper


class CommonService:
    def __init__(self, model):
        self.Model = model

    def create(self, args: dict) -> dict:
        new_model = self.Model(**args)
        new_model.save()
        return self.rm_id_prefix(new_model.to_mongo())

    def get_one_resource(self, where=None, model=None):
        if not where:
            where = {}
        if not model:
            model = self.Model
        try:
            return self.rm_id_prefix(model.objects.get(**where).to_mongo())
        except DoesNotExist:
            raise ResourceNotExistError(model.__class__.__name__, where)

    def retrieve(self, where=None, page=None, page_size=None, order_by=None, asc=False):
        if not where:
            where = {}
        obj_from, obj_to = None, None
        if page and page_size:
            obj_from, obj_to = (page - 1) * page_size, page * page_size
        if order_by:
            order = order_by
            if not asc:
                order = f"-{order}"
            objects = self.Model.objects(**where).order_by("state", order)[
                obj_from:obj_to
            ]
        else:
            objects = self.Model.objects(**where)[obj_from:obj_to]
        return self.rm_id_prefix([o.to_mongo() for o in objects])

    def get_model_by_id(self, mid: str, model=None, **extras: dict):
        if model is None:
            model = self.Model
        try:
            return model.objects.get(id=mid, **extras)
        except DoesNotExist:
            raise ResourceNotExistError(model.__class__.__name__, str((mid, extras)))

    def get_resource_by_id(self, mid: str, model=None, **extras: dict) -> dict:
        return self.rm_id_prefix(self.get_model_by_id(mid, model, **extras).to_mongo())

    def update(self, mid: str, updated_data: dict, **extras) -> dict:
        model = self.get_model_by_id(mid, **extras)
        model.update(**updated_data)
        model.reload()
        return self.rm_id_prefix(model.to_mongo())

    def remove(self, mid: str, **extras: dict) -> dict:
        return self.rm_id_prefix(self.update(mid, {"state": "inactive"}, **extras))

    def total(self, where: dict) -> int:
        return self.Model.objects(**where).count()

    def list(self, name: str, where: dict, page_args: dict) -> dict:
        fuzzy_where = {f"{k}__contains": v for k, v in where.items()}

        page = page_args.get("page", 1)
        page_size = page_args.get("page_size", 10)
        order_by = page_args.get("order_by") or "id"
        asc = page_args.get("asc", False)

        data = self.retrieve(fuzzy_where, page, page_size, order_by, asc)
        return paginated_wrapper(name, data, self.total(fuzzy_where), page, page_size)

    @staticmethod
    def rm_id_prefix(elements: Union[list, dict]):
        if isinstance(elements, dict):
            elements["id"] = str(elements["_id"])
            del elements["_id"]
            return elements
        else:
            rs = []
            for e in elements:
                _id = e.get("_id")
                if _id:
                    e["id"] = str(_id)
                    del e["_id"]
                rs.append(e)
            return rs
