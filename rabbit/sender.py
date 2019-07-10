import aio_pika
import asyncio
import pika
from config import mq_host
from config import mq_password
from config import mq_user
from config import mq_port


async def async_msg_local(loop):
    # Perform connection
    async with await aio_pika.connect('amqp://guest:guest@localhost/', loop=loop) as connection:
        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(b'Hello World'),
            routing_key='hello',
        )

        print('[x] Sent "Hello World"')


def sync_msg_local():
    with pika.BlockingConnection(pika.ConnectionParameters('amqp://guest:guest@localhost/')) as connection:
        channel = connection.channel()

        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body='sync Hello World!')
        print(" [x] Sent 'Hello World!'")


def sync_msg_remote():
    credentials = pika.PlainCredentials(mq_user, mq_password)
    params = pika.ConnectionParameters(mq_host, mq_port, '/', credentials)
    with pika.BlockingConnection(params) as connection:
        channel = connection.channel()

        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body='sync Hello World!')
        print(" [x] Sent 'Hello World!'")


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(async_msg_local(loop))
    sync_msg_remote()
