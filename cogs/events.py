from discord.ext import commands
from datetime import datetime


class EventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Called when the client is done preparing the data received from Discord. Usually after login is successful and
        the Client.guilds and co. are filled up.
        Warning
        This function is not guaranteed to be the first event called. Likewise, this function is not guaranteed to only
        be called once. This library implements reconnection logic and thus will end up calling this event whenever a
        RESUME request fails.

        :return:
        """
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print(datetime.now().strftime('%m/%d/%y %H:%M:%S'))
        print('------')


def setup(bot):
    bot.add_cog(EventsCog(bot))
