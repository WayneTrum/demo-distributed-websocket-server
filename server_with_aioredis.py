from sanic import Sanic
import asyncio
import aioredis
import uvloop


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
app = Sanic(__name__)
loop = asyncio.get_event_loop()


async def publish(ws):
    redis = await aioredis.create_redis("redis://localhost")
    while True:
        data = await ws.recv()
        await redis.publish_json('chan:1', data)


async def subscribe(ws):
    redis = await aioredis.create_redis('redis://localhost/0')
    channel = (await redis.subscribe('chan:1'))[0]
    while await channel.wait_message():
        msg = await channel.get_json()
        await ws.send(msg)


@app.websocket("join")
async def join_roome(request, ws):
    await asyncio.gather(publish(ws), subscribe(ws))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
