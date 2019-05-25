# -*- coding: utf-8 -*-
from flask import jsonify

from src.common.resources import cat_manager, cat_list_parser, common_parser
from src.module.cat.controller import CatListController, CatController

routes = {
    "/cats": (CatListController, [cat_manager, cat_list_parser]),
    "/cats/<string:cat_id>": (CatController, [cat_manager, common_parser]),
}
function_routes = {"/": lambda: jsonify({"hello": "world"})}
