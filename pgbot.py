from discord.ext import commands
import asyncpg
import config
import logging

from cogs import asyncpg_events


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(name)-15s %(message)s')
    return logger


class AsyncPgBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='!')
        self.pg = None
        self.logger = get_logger(self.__class__.__name__)
        self.load_extension('cogs.events')
        self.load_extension('cogs.error_handler')
        self.load_extension('cogs.commands')
        self.load_extension('cogs.asyncpg_events')

    async def on_connect(self):
        if not self.pg:
            self.pg = await asyncpg.connect(host=config.pg_host, user=config.pg_user, password=config.pg_password,
                                            database=config.pg_database)

    def load_extension(self, name):
        super().load_extension(name)
        self.logger.info('Successfully loaded extension {0}'.format(name))

    async def close(self):
        await self.pg.close()
        await super().close()
