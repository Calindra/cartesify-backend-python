import requests

class AppOptions:

    def __init__(self, url: str, broadcast_advance_requests: bool):
        self.url = url
        self.broadcast_advance_requests = broadcast_advance_requests


class App:

    def __init__(self, options: AppOptions):
        self.options = options
        self.advance_handlers = []
        self.inspect_handlers = []

    async def handle_advance(self, data):
        print("handle_advance", data)

    async def handle_inspect(self, data):
        print("handle_inspect", data)

    def add_advance_handler(self, handler):
        self.advance_handlers.append(handler)

    def add_inspect_handler(self, handler):
        self.inspect_handlers.append(handler)

    async def start(self):
        status = "accept"
        while True:
            response = requests.post(f'{self.options.url}/finish', data={
                'body': {'status': status},
                'parseAs': "text"
            })

            if response.status_code == 200:
                data = response.json()

                if data['request_type'] == 'advance_state':
                    status = await self.handle_advance(data['data'])
                    break

                if data['request_type'] == 'advance_state':
                    await self.handle_inspect(data['data'])
                    break

            elif response.status_code == 202:
                print("No rollup request available")
