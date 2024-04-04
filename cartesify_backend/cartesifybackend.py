import json
import requests
import logging
from .appfactory import AppFactory

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

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
        logger.info("App created")

        app.add_advance_handler(self.handle_advance)

        logger.info("Advance Handler added")

        app.add_inspect_handler(self.handle_inspect)

        logger.info("Inspect Handler added")

        return app


    def handle_inspect(self, data, rollups_url):
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

                response = requests.get(url)

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

                response_report = requests.post(f"{rollups_url}/report", json={"payload": hex_payload}, headers={"Content-Type": "application/json"})

                return "accept"
            return "reject"

        except Exception as e:
            print(e)
            print("Sending reject")
            # error_message = e.args[0] if len(e.args) > 0 else "Unexpected Error"
            # error_json = json.dumps({"error": {"message": error_message}})
            # buffer = bytes(error_json, "utf8")
            # hex_payload = "0x" + buffer.hex()
            # rollup.report(hex_payload)
            return "reject"

    def handle_advance(self, data, rollups_url):
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

                response = requests.request(url=cartesify_data['url'], method=cartesify_data['method'], headers=cartesify_data['headers'], json=cartesify_data['body'])

                response_data = {
                    "success": {
                        "data": response.json(),
                        "headers": dict(response.headers),
                        "status": response.status_code
                    }
                }

                # Converte o dicionário em uma string JSON
                jsonString = json.dumps(response_data)

                # Converte a string JSON para bytes usando UTF-8
                json_bytes = jsonString.encode('utf-8')

                # Converte os bytes para uma representação hexadecimal
                hex_payload = '0x' + json_bytes.hex()

                requests.post(f"{rollups_url}/report", json={"body": hex_payload},
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
            requests.post(f"{rollups_url}/report", json={"body": hex_payload},
                          headers={"Content-Type": "application/json"})

            return "reject"





