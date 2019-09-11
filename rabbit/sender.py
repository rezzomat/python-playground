import aio_pika
from aio_pika import ExchangeType
import pika
import json
from enum import Enum
from config import mq_host
from config import mq_password
from config import mq_user
from config import mq_port


class Guilds(Enum):
    ASM = 327585223112130570
    TEST = 234755524145446912


class Channels(Enum):
    OFFICER_LOUNGE = 441342971842134016
    LEADERSHIP_CHAT = 460905527145398292
    ASM_BOT_TESTING = 402570847363006475
    MEME_CHANNEL = 413375019939528704
    STAFF_NEED_HELP = 430105541629444098
    MOD_CHAT = 422853513924706304
    TESTING_SERVER_CHANNEL = 350506185092366336


async def async_msg_local(loop):
    """Sends a message locally

    :param loop:
    :return:
    """
    # Perform connection
    connection_string = f'amqp://{mq_user}:{mq_password}@{mq_host}:{mq_port}//asm'
    async with await aio_pika.connect(connection_string, loop=loop) as connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange('amq.topic', ExchangeType.TOPIC, durable=True)

        # asm guild: 327585223112130570
        # officer lounge: 441342971842134016
        # leadership: 460905527145398292
        # test: 402570847363006475

        # test guild: 234755524145446912
        # channel: 350506185092366336
        msg = "I agree, \\@208289854038081567> truly is the best."
        payload_dict = {
            "guild": Guilds.TEST.value,
            "channel": Channels.TESTING_SERVER_CHANNEL.value,
            "body": msg
        }
        payload = json.dumps(payload_dict).encode('utf-8')
        await exchange.publish(
            aio_pika.Message(payload),
            routing_key='century',
        )

        print('[x] Sent: ' + str(payload_dict))


def sync_msg_local():
    with pika.BlockingConnection(pika.ConnectionParameters('amqp://guest:guest@localhost/')) as connection:
        channel = connection.channel()
        channel.exchange_declare('amq.topic', exchange_type='topic', durable=True)

        channel.basic_publish(exchange='amq.topic',
                              routing_key='hello',
                              body='sync Hello World!')
        print(" [x] Sent 'Hello World!'")


def sync_msg_remote():
    credentials = pika.PlainCredentials(mq_user, mq_password)
    params = pika.ConnectionParameters(mq_host, mq_port, '/asm', credentials)
    with pika.BlockingConnection(params) as connection:
        channel = connection.channel()
        channel.exchange_declare(exchange='amq.topic', exchange_type='topic', durable=True)

        channel.basic_publish(exchange='amq.topic',
                              routing_key='asd.test',
                              body='sync Hello World!')
        print(" [x] Sent 'Hello World!'")


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(async_msg_local(loop))
    sync_msg_remote()
