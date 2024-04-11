This package is intended to be used with [@calindra/cartesify](https://www.npmjs.com/package/@calindra/cartesify).


```python
import asyncio
import logging
from cartesify_backend import CartesifyBackend, CartesifyOptions
from quart import Quart, request, jsonify
import json


app = Quart(__name__)

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

port = 8383

games = []

@app.route('/health', methods=['GET'])
async def your_endpoint():
    logger.info("Requisição recebida no endpoint your-endpoint")
    print("Requisição recebida no endpoint your-endpoint")
    sender_address = request.headers.get('x-msg_sender')
    response_data = {'games': str(games)}
    logger.info(f'response is {response_data}')
    return jsonify(response_data)

@app.route('/new-game', methods=['POST'])
async def new_game():
    logger.info("Requisição recebida no endpoint new_game")
    print("Requisição recebida no endpoint new-game")
    sender_address = request.headers.get('x-msg_sender')
    commit = json.loads(await request.get_json())
    print(f"type of commit {type(commit)}")
    games.append({'player1': sender_address, 'commit1': commit['any']})
    return jsonify({'created': len(games)})

async def main():
    try:
        logger.info(f'Initiating app')

        options = CartesifyOptions(url='', broadcast_advance_requests=False)
        cartesify_app = CartesifyBackend().create_app(options)

        await asyncio.gather(app.run_task(port=port, host='0.0.0.0'), cartesify_app.start())

    except Exception as e:
        print(e)
        logger.error(e)

if __name__ == '__main__':
    asyncio.run(main())

```