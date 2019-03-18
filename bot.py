import discord
import traceback
import config

from models import initialize_sql
from discord.ext import commands


cogs_extensions = [
    "cogs.events",
    "cogs.commands",
    "cogs.error_handler"
]

bot = commands.Bot(command_prefix='$',
                   description='playground')

if __name__ == "__main__":

    initialize_sql('', None)

    for extension in cogs_extensions:
        try:
            bot.load_extension(extension)
            print('Successfully loaded extension {0}'.format(extension))
        except (discord.ClientException, ModuleNotFoundError):
            print('Failed to load extension {0}.'.format(extension))
            traceback.print_exc()

    bot.run(config.bot_token, bot=True, reconnect=True)
