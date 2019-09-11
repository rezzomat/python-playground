from discord.ext import commands
import asyncio
from aio_pika import connect, IncomingMessage, ExchangeType

from config import mq_host
from config import mq_password
from config import mq_user
from config import mq_port


class Log:
    def __init__(self, pg):
        self.pg = pg

    async def insert(self, level, info):
        await self.pg.execute("INSERT INTO log (date, level, record) VALUES (CURRENT_TIMESTAMP, $1, $2)", level, info)


class AsyncPgEvents(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        # self.bot.loop.create_task(self.init_rabbitMq(self.bot.loop))
        self.bot.loop.create_task(self.on_test())
        self.log = Log(self.bot.pg)

    async def init_rabbitMq(self, loop):
        await self.bot.wait_until_ready()
        # Connect to RabbitMQ
        connection_string = f'amqp://{mq_user}:{mq_password}@{mq_host}:{mq_port}/'
        connection = await connect(connection_string, loop=loop)
        mq_channel = await connection.channel()
        exchange = await mq_channel.declare_exchange('amq.topic', ExchangeType.TOPIC, durable=True)

        queue = await mq_channel.declare_queue('century')
        await queue.bind(exchange=exchange, routing_key='century')

        # Start listening to queue
        await queue.consume(self.test_mq, no_ack=True)

    async def on_test(self, *args):
        queue = asyncio.Queue(loop=self.bot.loop)

        def listener(*args):
            self.bot.logger.info('event triggered: ' + str(args))
        await self.bot.pg.add_listener('test', listener)

        event = await queue.get()
        self.bot.logger.info(event)

    # RabbitMQ
    async def test_mq(self, message: IncomingMessage):
        await self.log.insert('INFO', 'testing')
        print('Got a RabbitMQ message:')
        print(message)
        print(message.body)


def setup(bot):
    bot.add_cog(AsyncPgEvents(bot))
