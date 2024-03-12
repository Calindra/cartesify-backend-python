from appfactory import AppFactory
class CartesifyOptions:
    
    def __init__(self, url: str, broadcast_advance_requests: bool):
        self.url = url
        self.broadcast_advance_requests = broadcast_advance_requests

    def __str__(self):
        return f'CartesifyOptions: url={self.url}, broadcast_advance_requests={self.broadcast_advance_requests}'


class CartesifyBackend:

    def create_app(self, options: CartesifyOptions):
        factory = AppFactory()
        app = factory.create_dapp(options)

        app.add_advance_handler()
        pass



