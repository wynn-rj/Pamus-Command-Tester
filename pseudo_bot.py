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
        self._after_invoke = None
        self._before_invoke = None

    def add_listener(self, func, name=None):
        pass

    async def can_run(self, ctx, *, call_once=False):
        return True

    def add_check(self, func, *, call_once=False):
        self._checks.append(func)

    def add_cog(self, cog):
        cog = cog._inject(self)
        self._cogs[cog.__cog_name__] = cog

    def run_command(self, message):
        view = StringView(message.content)
        ctx = PseudoContext(prefix=None, view=view, bot=self, message=message)
        invoker = view.get_word()
        ctx.invoked_with = invoker
        ctx.prefix = None
        ctx.command = self.all_commands.get(invoker)
        if ctx.command is not None:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(ctx.command.invoke(ctx))
        elif ctx.invoked_with:
            raise CommandNotFound(f'Command {ctx.invoked_with} is not found')

