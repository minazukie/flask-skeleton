# -*- coding: utf-8 -*-
import logging
import traceback
from http import HTTPStatus

from mongoengine.errors import ValidationError, FieldDoesNotExist, DoesNotExist
from dataclasses_jsonschema import ValidationError as JsonSchemaValidationError
from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException


class ApiBaseError(Exception):
    code = 500
    message = "internal server error"
    extras = None

    def to_dict(self):
        return {"code": self.code, "message": self.message}


class RequiredColumnNotExistError(ApiBaseError):
    code = 400
    extras = None

    def __init__(self, key):
        self.message = f"column `{key}`` is missing"


class ResourceNotExistError(ApiBaseError):
    code = 400
    message = "does not exist"
    extras = None

    def __init__(self, resource: str, resource_id: str):
        self.message = f"{resource} {resource_id} {self.message}"


def error_handle(e):
    if current_app.debug:
        traceback.print_exc()
    if isinstance(e, HTTPException):
        return jsonify({"code": e.code, "message": e.description}), e.code
    elif isinstance(e, ApiBaseError):
        return jsonify(e.to_dict()), e.code
    elif isinstance(e, FieldDoesNotExist):
        return jsonify({"code": 400, "message": str(e)}), HTTPStatus.BAD_REQUEST
    elif isinstance(e, DoesNotExist):
        return jsonify({"code": 404, "message": str(e)}), HTTPStatus.NOT_FOUND
    elif isinstance(e, ValidationError):
        return jsonify({"code": 400, "message": e.message}), HTTPStatus.BAD_REQUEST
    elif isinstance(e, JsonSchemaValidationError):
        return jsonify({"code": 400, "message": str(e).split('\n\n')[0]}), HTTPStatus.BAD_REQUEST
    else:
        logging.error("an unexpected error occurred")
        logging.error(traceback.format_exc())
        return jsonify({"code": 500, "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
