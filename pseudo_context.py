from discord.ext.commands.context import Context

class PseudoContext(Context):
    async def send(self, content=None, *, tts=False, embed=None, file=None,
                   files=None, delete_after=None, nonce=None,
                   allowed_mentions=None):
        print(content)
