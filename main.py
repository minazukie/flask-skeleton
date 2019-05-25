from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer  # noqa
import logging  # noqa
from src.app import AppFactory  # noqa


def bootstrap():
    port = 5000
    http_server = WSGIServer(("0.0.0.0", port), AppFactory.create(), log=logging.getLogger(__name__))
    logging.info(f"served at http://localhost:{port}/")
    http_server.serve_forever()


if __name__ == "__main__":
    bootstrap()
