from app import App
from app import AppOptions
import os
import socket
from urllib.parse import urlparse
from cartesi import DApp


class AppFactory:

    def create_dapp(self):
        dapp = DApp()
        return dapp

