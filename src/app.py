# -*- coding: utf-8 -*-
import logging

from flask import Flask
from flask_restful import Api
from mongoengine import connect

from src.common import settings
from src.common.routes import routes, function_routes
from src.common.exceptions import error_handle as eh


class AppFactory:
    def __init__(self, name=__name__):
        self.app_name = name
        self.app = self.new_app()

    def pre_create(self):
        connect(host=self.app.config["MONGO_URI"])
        return self

    def error_handle(self):
        @self.app.errorhandler(Exception)
        def error(e):
            return eh(e)

        return self

    def new_app(self) -> Flask:
        app = Flask(self.app_name, static_url_path="/api/static")
        app.config.from_object(settings)
        app.secret_key = "my-key"

        return app

    def handle_api(self) -> Api:
        api = Api(self.app, prefix="/api/v1")
        for url, resource in routes.items():
            if isinstance(resource, tuple) or isinstance(resource, list):
                resource_class, resource_args = resource
                api.add_resource(
                    resource_class, url, resource_class_args=tuple(resource_args)
                )
            elif isinstance(resource, dict):
                resource_class, resource_args = resource
                api.add_resource(
                    resource_class, url, resource_class_kwargs=resource_args
                )
            else:
                api.add_resource(resource, url)
        for url, value in function_routes.items():
            if isinstance(value, tuple):
                methods, func = value
            else:
                methods = ["GET"]
                func = value
            self.app.add_url_rule(url, url, view_func=func, methods=methods)
        return api

    def basic_handle(self):
        self.handle_api()
        return self

    @classmethod
    def create(cls) -> Flask:
        factory = cls().pre_create().basic_handle().error_handle()
        logging.info("running...")
        return factory.app
