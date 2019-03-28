# Example of distributed websocket server

## Link

- [sanic web framework](<https://github.com/huge-success/sanic>)
- [aioredis](<https://github.com/aio-libs/aioredis>)
- [aio_pika](<https://github.com/mosquito/aio-pika>)
- [asyncio.gather](<https://docs.python.org/zh-cn/3/library/asyncio-task.html#id7>)

## Run

- Install pipenv
- Run `pipenv install` 
- Run `pipenv shell` 
- Run `python server_with_aioredis.py ` to start server which use redis
- Run `python server_with_aiopika.py ` to start server which use rabbitmq

## Notice

- This project is just a demo, don't Shanggangshangxian.
- Before start server please change `RABBITMQ_URL` or `REDIS_URL` to youself value.
