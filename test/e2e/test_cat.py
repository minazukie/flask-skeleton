# -*- coding: utf-8 -*-
import time
from unittest.mock import patch

from test import settings

patch("src.common.settings", new=settings).start()  # noqa

from src.app import AppFactory
from src.module.models import Cat


class TestCat:
    @staticmethod
    def init_mock_data():
        Cat(
            name="test_kitty",
            age=1,
            gender=1,
            birthday=int(time.time()),
            state="active",
            created_at=int(time.time()),
            updated_at=int(time.time()),
        ).save()

    def setup(self):
        self.app = AppFactory.create().test_client()
        self.init_mock_data()

    def test_list_all_cats(self):
        res = self.app.get("/api/v1/cats")
        assert res.is_json
        assert res.status_code == 200
        assert res.json["total"] == 1
        assert res.json["cats"][0]["name"] == "test_kitty"
