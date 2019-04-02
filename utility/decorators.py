from discord.ext import commands
import functools
from utility.logger import logger


def is_bot():
    async def predicate(ctx):
        return ctx.message.author.bot
    return commands.check(predicate)


def log():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args):
            logger.debug('', extra={'command': func.__name__, 'action': 'enter'})
            await func(*args)
            logger.debug('', extra={'command': func.__name__, 'action': 'exit'})
        return wrapped
    return wrapper


class LogCommand(object):
    def __init__(self, f):

        self.f = f

    def __call__(self, *args):
        print('enter ', self.f.__name__)
        self.f(*args)
        print('exit ', self.f.__name__)

