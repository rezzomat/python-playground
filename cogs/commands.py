from discord.ext import commands
from utility import decorators


class CommandsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test")
    @decorators.log()
    async def test(self, ctx):
        await ctx.send("$asdf")

    @commands.command(name="asdf")
    @decorators.is_bot()
    async def asdf(self, ctx):
        await ctx.send("success")


def setup(bot):
    bot.add_cog(CommandsCog(bot))
