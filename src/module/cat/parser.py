# -*- coding: utf-8 -*-
from src.module.parsers import CommonRequestParser


class CatListParser(CommonRequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument("page", type=int, default=1)
        self.add_argument("page_size", type=int, default=10)
        self.add_argument("order_by", type=str, default="id")
        self.add_argument("asc", type=bool, default=False)
        self.add_argument("name", type=str, default="")
        self.add_argument("state", type=str, default="")
