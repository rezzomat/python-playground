from discord.ext import commands
import asyncio
from aio_pika import connect, IncomingMessage

from config import mq_host
from config import mq_password
from config import mq_user
from config import mq_port


class AsyncPgEvents(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.init_rabbitMq(self.bot.loop))

    async def init_rabbitMq(self, loop):
        await self.bot.wait_until_ready()
        # Connect to RabbitMQ
        connection_string = f'amqp://{mq_user}:{mq_password}@{mq_host}:{mq_port}/'
        connection = await connect(connection_string, loop=loop)
        mq_channel = await connection.channel()
        queue = await mq_channel.declare_queue('hello')

        # Start listening to queue
        await queue.consume(self.test_mq, no_ack=True)

    async def on_test(self, *args):
        queue = asyncio.Queue(loop=self.bot.loop)

        def listener(*args):
            self.bot.logger.info('event triggered: ' + event)
        await self.bot.pg.add_listener('test', listener)

        event = await queue.get()

    # RabbitMQ
    async def test_mq(self, message: IncomingMessage):
        print('Got a RabbitMQ message:')
        print(message)
        print(message.body)


def setup(bot):
    bot.add_cog(AsyncPgEvents(bot))
