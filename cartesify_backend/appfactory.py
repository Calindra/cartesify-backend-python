from .App import App, AppOptions
import os
import socket
from urllib.parse import urlparse
import logging

NONODO_HTTP_SERVER_URL = urlparse('http://127.0.0.1:8080/rollup')
DEFAULT_ROLLUP_HTTP_SERVER_URL = urlparse('http://127.0.0.1:5004')

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class AppFactory:

    def is_port_open(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(1)

        try:
            server.bind(('127.0.0.1', port))
        except socket.error as e:
            if e.errno == socket.errno.EADDRINUSE:
                # Port is in use
                return True
            else:
                # Other error occurred
                raise e
        finally:
            server.close()

        # Port is available
        return False

    def create_dapp(self, options):

        if options.url != "":
            logger.info(f"Connecting to {options.url}")
            print(f"Connecting to {options.url}")
            return App(AppOptions(options.url, options.broadcast_advance_requests))

        ROLLUP_HTTP_SERVER_URL = os.getenv('ROLLUP_HTTP_SERVER_URL', '')

        if ROLLUP_HTTP_SERVER_URL != "":
            logger.info(f"Connections to Rollup HTTP Server: {ROLLUP_HTTP_SERVER_URL.geturl()}")
            return App(AppOptions(ROLLUP_HTTP_SERVER_URL, options.broadcast_advance_requests))

        if (self.is_port_open(NONODO_HTTP_SERVER_URL.port)):
            logger.info(f"Connections to Nonodo: {NONODO_HTTP_SERVER_URL.geturl()}")
            return App(AppOptions(NONODO_HTTP_SERVER_URL.geturl(), options.broadcast_advance_requests))

        if (self.is_port_open(DEFAULT_ROLLUP_HTTP_SERVER_URL.port)):
            logger.info(f"Connections to Default Rollup HTTP_SERVER: {DEFAULT_ROLLUP_HTTP_SERVER_URL.geturl()}")
            return App(AppOptions(DEFAULT_ROLLUP_HTTP_SERVER_URL.geturl(), options.broadcast_advance_requests))