import json
import requests
import logging
from .appfactory import AppFactory
import httpx

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class CartesifyOptions:

    def __init__(self, url: str, broadcast_advance_requests: bool):
        self.url = url
        self.broadcast_advance_requests = broadcast_advance_requests


    def __str__(self):
        return f'CartesifyOptions: url={self.url}, broadcast_advance_requests={self.broadcast_advance_requests}'

class CartesifyBackend:

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10)

    def create_app(self, options: CartesifyOptions):
        factory = AppFactory()
        app = factory.create_dapp(options)
        logger.info("App created")

        app.add_advance_handler(self.handle_advance)

        logger.info("Advance Handler added")

        app.add_inspect_handler(self.handle_inspect)

        logger.info("Inspect Handler added")

        return app


    async def handle_inspect(self, data, rollups_url):
        logger.info("Cartesify handle inspect")
        payload = data['payload']
        try:
            if not payload.startswith('0x7b22'):
                return "reject"

            hex_string = payload.replace('0x', '')
            byte_buffer = bytes.fromhex(hex_string)
            utf8_string = byte_buffer.decode('utf-8')
            json_data = json.loads(utf8_string)

            print(f"json_data {json_data}")

            if 'cartesify' in json_data:
                url = json_data['cartesify']['fetch']['url']

                try:
                    response = await self.client.get(url)

                    json_data = response.json()

                    response_data = {
                        "success": {
                            "text": json.dumps(json_data),
                            "data": json_data,
                            "headers": [[key, value] for key, value in response.headers.items()],
                            "status": response.status_code
                        }
                    }
                    # Converte o dicionário em uma string JSON
                    jsonString = json.dumps(response_data)

                    # Converte a string JSON para bytes usando UTF-8
                    json_bytes = jsonString.encode('utf-8')

                    # Converte os bytes para uma representação hexadecimal
                    hex_payload = '0x' + json_bytes.hex()

                    response_report = await self.client.post(f"{rollups_url}/report", json={"payload": hex_payload}, headers={"Content-Type": "application/json"})

                    return "accept"
                except Exception as e:
                    logger.error("Excecao generica")
                except httpx.HTTPStatusError as e:
                    print(f'Erro ao iniciar cartesify {e}')

            return "reject"

        except Exception as e:
            print(e)
            print("Sending reject")
            error_message = e.args[0] if len(e.args) > 0 else "Unexpected Error"
            error_json = json.dumps({"error": {"message": error_message}})
            buffer = bytes(error_json, "utf8")
            hex_payload = "0x" + buffer.hex()
            await self.client.post(f"{rollups_url}/report", json={"payload": hex_payload},
                                   headers={"Content-Type": "application/json"})
            return "reject"

    async def handle_advance(self, data, rollups_url):
        logger.info("Cartesify handle advance")
        payload = data['payload']
        try:
            if not payload.startswith('0x7b22'):
                return "reject"

            hex_string = payload[2:]  # Remove o prefixo '0x'
            buffer = bytes.fromhex(hex_string)

            # Converta o buffer para uma string utf-8
            utf8_string = buffer.decode('utf-8')

            json_data = json.loads(utf8_string)

            if 'cartesify' in json_data:
                cartesify_data = json_data['cartesify']

                logger.info(f'Cartesify Data {cartesify_data}')

                method = cartesify_data['fetch']['options']['method']

                request = httpx.Request(method=method, url=cartesify_data['fetch']['url'], headers=cartesify_data['fetch']['options']['headers'], json=cartesify_data['fetch']['options']['body'])

                response = await self.client.send(request)

                json_data = response.json()

                response_data = {
                    "success": {
                        "text": json.dumps(json_data),
                        "data": json_data,
                        "headers": [[key, value] for key, value in response.headers.items()],
                        "status": response.status_code
                    }
                }

                # Converte o dicionário em uma string JSON
                json_string = json.dumps(response_data)

                # Converte a string JSON para bytes usando UTF-8
                json_bytes = json_string.encode('utf-8')

                # Converte os bytes para uma representação hexadecimal
                hex_payload = '0x' + json_bytes.hex()

                await self.client.post(f"{rollups_url}/report", json={"payload": hex_payload},
                              headers={"Content-Type": "application/json"})

                return "accept"

            return "reject"

        except Exception as e:
            print(e)
            print("Sending reject")
            error_message = e.args[0] if len(e.args) > 0 else "Unexpected Error"
            error_json = json.dumps({"error": {"message": error_message}})
            buffer = bytes(error_json, "utf8")
            hex_payload = "0x" + buffer.hex()
            await self.client.post(f"{rollups_url}/report", json={"payload": hex_payload},
                          headers={"Content-Type": "application/json"})

            return "reject"





