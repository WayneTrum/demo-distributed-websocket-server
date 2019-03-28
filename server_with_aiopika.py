from sanic import Sanic
import asyncio
import aio_pika
import uvloop
import json

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
app = Sanic(__name__)
loop = asyncio.get_event_loop()

RABBITMQ_URL = "amqp://example:example_password@host:port"
QUEUE_NO = 0


async def publish(ws):
    connection = await aio_pika.connect_robust(
        RABBITMQ_URL
    )
    routing_key = "test_queue"
    channel = await connection.channel()
    exchange = await channel.declare_exchange('direct', auto_delete=True)
    while True:
        data = await ws.recv()
        print(data)
        await exchange.publish(
            aio_pika.Message(
                body=json.dumps(data).encode()
            ),
            routing_key=routing_key
        )


async def subscribe(ws):
    connection = await aio_pika.connect_robust(
        RABBITMQ_URL
    )
    queue_name = "test_queue_" + str(QUEUE_NO)
    routing_key = "test_queue"
    channel = await connection.channel()
    exchange = await channel.declare_exchange('direct', auto_delete=True)
    queue = await channel.declare_queue(queue_name, auto_delete=True)
    await queue.bind(exchange, routing_key)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                print(message.body)
                await ws.send(json.loads(message.body))
                if queue.name in message.body.decode():
                    break


@app.websocket("join")
async def join_roome(request, ws):
    global QUEUE_NO
    QUEUE_NO += 1
    await asyncio.gather(publish(ws), subscribe(ws))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
