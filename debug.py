# -*- coding: utf-8 -*-
import logging

logging.basicConfig(level=logging.DEBUG)

from flask import Flask  # noqa
from flask_failsafe import failsafe  # noqa
import os  # noqa

os.environ["FLASK_ENV"] = "development"
os.environ["FLASK_DEBUG"] = "True"
os.environ["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__))


@failsafe
def start_debug() -> Flask:
    from src.app import AppFactory
    return AppFactory.create()


if __name__ == "__main__":
    app = start_debug()
    app.run(host="localhost", port="4396")
