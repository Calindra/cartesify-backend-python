import requests
import logging
import httpx

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

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
        result = await self.advance_handlers[0](data, self.options.url)
        return result

    async def handle_inspect(self, data):
        return await self.inspect_handlers[0](data, self.options.url)

    def add_advance_handler(self, handler):
        self.advance_handlers.append(handler)

    def add_inspect_handler(self, handler):
        self.inspect_handlers.append(handler)

    async def start(self):
        logger.info("App initiating")
        status = "accept"
        client = httpx.AsyncClient(timeout=10)
        while True:
            try:

                response = await client.post(
                      f"{self.options.url}/finish",
                       json={"status": status},
                       headers={"Content-Type": "application/json"}
                )

                if response.status_code == 200:
                    data = response.json()

                    if data['request_type'] == 'advance_state':
                        status = await self.handle_advance(data['data'])

                    elif data['request_type'] == 'inspect_state':
                        await self.handle_inspect(data['data'])

                elif response.status_code == 202:
                    logger.info("No rollup request available")
            except Exception as e:
                logger.error(f'Error starting cartesify {e}')
