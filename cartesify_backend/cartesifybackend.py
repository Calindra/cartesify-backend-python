import json
import requests
import logging
from .appfactory import AppFactory
from cartesi import Rollup, RollupData

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

def dapp_inspect_decorator(func):
    def wrapper(self, *args, **kwargs):
        return self.dapp.inspect()
    return wrapper

def dapp_advance_decorator(func):
    def wrapper(self, *args, **kwargs):
        return self.dapp.advance()
    return wrapper

class CartesifyBackend:

    def __init__(self):
        logger.info("Starting Cartesify App")
        self.dapp = AppFactory().create_dapp()
    def get_app(self):
        return self.dapp

    @dapp_inspect_decorator
    def handle_inspect(self, rollup:Rollup, data: RollupData) -> bool:
        logger.info("Cartesify handle inspect")
        try:
            payload = data.str_payload()

            hex_string = payload.replace('0x', '')
            byte_buffer = bytes.fromhex(hex_string)
            utf8_string = byte_buffer.decode('utf-8')
            json_data = json.loads(utf8_string)

            if 'cartesify' in json_data:
                cartesify_data = json_data['cartesify']

                resp = requests.request(cartesify_data)

                return True
            return False

        except Exception as e:
            print(e)
            print("Sending reject")
            error_message = e.args[0] if len(e.args) > 0 else "Unexpected Error"
            error_json = json.dumps({"error": {"message": error_message}})
            buffer = bytes(error_json, "utf8")
            hex_payload = "0x" + buffer.hex()
            rollup.report(hex_payload)
            return False

    @dapp_advance_decorator
    def handle_advance(self, rollup:Rollup, data: RollupData) -> bool:
        logger.info("Cartesify handle advance                                       ")

        try:
            payload = data.str_payload()
            if not payload.startswith('0x7b22'):
                return False

            hex_string = payload[2:]  # Remove o prefixo '0x'
            buffer = bytes.fromhex(hex_string)

            # Converta o buffer para uma string utf-8
            utf8_string = buffer.decode('utf-8')

            json_data = json.loads(utf8_string)

            if 'cartesify' in json_data:
                cartesify_data = json_data['cartesify']

                resp = requests.request(cartesify_data)

                json_string = json.dumps({
                    'success': {
                        'data': resp.json(),
                        'headers': dict(resp.headers),
                        'status': resp.status_code
                    }
                })

                # Converta para bytes
                byte_buffer = json_string.encode("utf-8")

                # Converta para hexadecimal
                hex_payload = "0x" + byte_buffer.hex()

                rollup.report(hex_payload)

                return True

            return False

        except Exception as e:
            print(e)
            print("Sending reject")
            error_message = e.args[0] if len(e.args) > 0 else "Unexpected Error"
            error_json = json.dumps({"error": {"message": error_message}})
            buffer = bytes(error_json, "utf8")
            hex_payload = "0x" + buffer.hex()
            rollup.report(hex_payload)
            return False





