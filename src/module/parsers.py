# -*- coding: utf-8 -*-
import typing
import math

import yaml

from flask_restful import reqparse
from flask import request
from werkzeug import exceptions

from src.common.exceptions import ApiBaseError


class InvalidFileFormatError(ApiBaseError):
    code = 400
    message = "invalid file format"

    def __init__(self, e):
        self.message = f"{self.message}：{e}"


class ValueParseError(ApiBaseError):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


def paginated_wrapper(
    resource_name: str, resources: list, total: int, page: int, page_size: int
) -> dict:
    return {
        "page": page,
        "pages": math.ceil(total / page_size),
        "count_per_page": page_size,
        "total": total,
        resource_name: resources,
    }


def parse_args(self, req=None, strict=False, http_error_code=400):
    """Parse all arguments from the provided request and return the results
        as a Namespace

        :param req: Can be used to overwrite request from Flask
        :param strict: if req includes args not in parser, throw 400 BadRequest exception
        :param http_error_code: use custom error code for `flask_restful.abort()`
        """
    if req is None:
        req = request

    namespace = self.namespace_class()

    # A record of arguments not yet parsed; as each is found
    # among self.args, it will be popped out
    req.unparsed_arguments = dict(self.argument_class("").source(req)) if strict else {}
    errors = {}
    for arg in self.args:
        value, found = arg.parse(req, self.bundle_errors)
        if isinstance(value, ValueError):
            errors.update(found)
            found = None
        if found or arg.store_missing:
            namespace[arg.dest or arg.name] = value
    if errors:
        raise ValueParseError(http_error_code, errors[list(errors.keys())[0]])

    if strict and req.unparsed_arguments:
        raise exceptions.BadRequest(
            "Unknown arguments: %s" % ", ".join(req.unparsed_arguments.keys())
        )

    return namespace


reqparse.RequestParser.parse_args = parse_args  # patch


class CommonRequestParser(reqparse.RequestParser):
    @staticmethod
    def json() -> dict:
        return request.json

    @staticmethod
    def data() -> typing.Any:
        return request.data

    @staticmethod
    def cookies() -> dict:
        return request.cookies

    @staticmethod
    def form() -> dict:
        return request.form.to_dict()

    @staticmethod
    def files():
        return request.files

    @staticmethod
    def content_type() -> str:
        return request.headers["content-type"]

    def split_args(
        self, args=None
    ) -> typing.Tuple[typing.Dict[str, typing.Any], typing.Dict[str, typing.Any]]:
        if not args:
            args = self.parse_args()
        where_args = dict(args)
        page_args = {}
        if "page" in where_args.keys():
            page_args["page"] = where_args.pop("page")
        if "page_size" in where_args.keys():
            page_args["page_size"] = where_args.pop("page_size")
        if "order_by" in where_args.keys():
            page_args["order_by"] = where_args.pop("order_by")
        if "asc" in where_args.keys():
            page_args["asc"] = where_args.pop("asc")
        return where_args, page_args

    def dump_file(self) -> str:
        file_obj = self.files().get("file")

        if not file_obj:
            file = ""
        else:
            file_tp = file_obj.filename.split(".")[-1].upper()
            file = file_obj.stream.read().decode(encoding="UTF-8")
            FileFormatChecker(file_tp, file).check()
        return file


class FileFormatChecker:
    def __init__(self, file_type: str, file: typing.Any):
        self.file_type = file_type
        self.file = file

    def check(self):
        self._check_yaml()

    def _check_yaml(self):
        if self.file_type.upper() in ("YAML", "YML"):
            try:
                yaml.load(self.file)
            except Exception as e:
                raise InvalidFileFormatError(e)
