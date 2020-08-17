import asyncio
from pseudo_context import PseudoContext

from discord.ext.commands.errors import *
from discord.ext.commands.core import GroupMixin, Command
from discord.ext.commands.view import StringView

class PseudoBot(GroupMixin):
    def __init__(self):
        super().__init__()
        self._checks = []
        self._cogs = {}

    def add_listener(self, func, name=None):
        pass

    def add_check(self, func, *, call_once=False):
        self._checks.append(func)

    def add_cog(self, cog):
        cog = cog._inject(self)
        self._cogs[cog.__cog_name__] = cog

    def run_command(self, message):
        view = StringView(message.content)
        ctx = PseudoContext(view=view, bot=self, message=message)
        invoker = view.get_word()
        ctx.invoked_with = invoker
        ctx.prefix = None
        ctx.command = self.all_commands.get(invoker)
        if ctx.command is not None:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.invoke_command(ctx))
            loop.close()
        elif ctx.invoked_with:
            raise CommandNotFound(f'Command {ctx.invoked_with} is not found')

    async def invoke_command(self, ctx):
        try:
            await ctx.command._parse_arguments(ctx)
            await ctx.command.call_before_hooks(ctx)
            ctx.invoke_subcommand = None
            ctx.subcommand_passed = None
            ret = await ctx.command.callback(*ctx.args, **ctx.kwargs)
        finally:
            await ctx.command.call_after_hooks(ctx)
        return ret
