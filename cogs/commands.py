from discord.ext import commands
from utility import decorators
import asyncio
import discord
import aiohttp


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

    @commands.command(name="flow")
    async def flow(self, ctx, *, title=None):
        if title is None:
            return await ctx.send("list")

        body = ''
        labels = []

        msg_1 = await ctx.send("title: {0}\r\nEnter body now:"
                               "\r\n"
                               "*skip: react with {1}*\r\n"
                               "*cancel: react with {2}*\r\n".format(title, '▶',
                                                                     '⏹'))
        await msg_1.add_reaction('▶')
        await msg_1.add_reaction('⏹')

        def reaction_check_msg_1(reaction, user):
            return user.id == ctx.author.id \
                   and str(reaction.emoji) in ['▶', '⏹'] \
                   and reaction.message.id == msg_1.id

        def message_check(message):
            return message.author.id == ctx.author.id and message.channel.id == ctx.message.channel.id

        done, pending = await asyncio.wait([
            self.bot.wait_for('message', check=message_check),
            self.bot.wait_for('reaction_add', check=reaction_check_msg_1)],
            return_when=asyncio.FIRST_COMPLETED)

        if done:
            result = done.pop().result()

            if isinstance(result, discord.Message):
                body = result.content
            else:
                reaction, user = result
                if reaction.emoji == '⏹':
                    return await ctx.send('Canceled')
                else:
                    body = ''

        msg_2 = await ctx.send('body: {0}\r\nEnter labels now: (comma separated)'
                               '\r\n'
                               '*skip: react with {1}*\r\n'
                               '*cancel: react with {2}*\r\n'.format(body, '▶', '⏹'))

        await msg_2.add_reaction('▶')
        await msg_2.add_reaction('⏹')

        def reaction_check_msg_2(reaction, user):
            return user.id == ctx.author.id \
                   and str(reaction.emoji) in ['▶', '⏹'] \
                   and reaction.message.id == msg_2.id

        done, pendig = await asyncio.wait([
            self.bot.wait_for('message', check=message_check),
            self.bot.wait_for('reaction_add', check=reaction_check_msg_2)],
            return_when=asyncio.FIRST_COMPLETED)

        if done:
            result = done.pop().result()

            if isinstance(result, discord.Message):
                labels = result.content.split(',')
            else:
                reaction, user = result
                if reaction.emoji == '⏹':
                    return await ctx.send('Canceled')
                else:
                    labels = []

        await ctx.send('Done\r\n'
                       'title: {0}\r\n'
                       'body: {1}\r\n'
                       'labels: {2}'.format(title, body, labels))
        """
        done, pending = await asyncio.wait([
                            bot.wait_for('message')
                            bot.wait_for('reaction_add')
                        ], return_when=asyncio.FIRST_COMPLETED)

        try:
            stuff = done.pop().result()
        except ...:
            # if any of the tasks died for any reason,
            #  the exception will be replayed here.
        """

    @commands.command(name="github")
    async def github(self, ctx):
        async with aiohttp.ClientSession() as session:
            response = await self.fetch(session, 'https://api.github.com/repos/naiii/python-playground/issues')
            await ctx.send(response)

    async def fetch(self, session, url):
        async with session.get(url) as response:
            r = await response.json()
            return [label['name'] for label in r]


def setup(bot):
    bot.add_cog(CommandsCog(bot))
