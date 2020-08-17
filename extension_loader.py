import importlib.util
from discord.ext import commands

class ExtensionLoader():
    def __init__(self, bot):
        self._extensions = []
        self.bot = bot

    def load_extension(self, name):
        if name in self._extensions:
            raise commands.ExtensionAlreadyLoaded(name)

        spec = importlib.util.find_spec(name)
        if spec is None:
            raise commands.ExtensionNotFound(name)

        lib = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(lib)
        except Exception as ex:
            raise commands.ExtensionFailed(name, ex) from ex

        try:
            setup = getattr(lib, 'setup')
        except AttributeError:
            raise commands.NoEntryPointError(name)

        try:
            setup(self.bot)
        except Exception as ex:
            raise commands.ExtensionFailed(name, ex) from ex
