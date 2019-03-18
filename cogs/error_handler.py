from discord.ext import commands


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        # prevent commands with local handler to be handled here
        if hasattr(ctx.command, 'on_error'):
            return

        # ignored = (commands.CommandNotFound, commands.UserInputError)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        # if isinstance(error, ignored):
        #     return

        if isinstance(error, commands.DisabledCommand):
            return await ctx.send('{0} has been disabled.'.format(ctx.command))

        elif isinstance(error, commands.CheckFailure):
            return await ctx.send('You don\'t have the permission to execute the command {0}'.format(ctx.command))

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send('{0} can not be used in Private Messages.'.format(ctx.command))
            except:
                pass
        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send(str(error))
        else:
            await ctx.send("command not found")


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
