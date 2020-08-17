import sys
import os
import argparse
import readline

from utils.config_reader import YAMLConfigReader
from pseudo_message import PseudoMessage
from extension_loader import ExtensionLoader
from pseudo_bot import PseudoBot
from discord.ext.commands.errors import *

class BotCli():
    def __init__(self):
        self.bot = PseudoBot()
        self.loader = ExtensionLoader(self.bot)
        self.command = ''

    def send_message(self, cmd):
        self.bot.run_command(PseudoMessage(cmd))

    def get_command(self):
        try:
            self.command = input('> ')
            return self.command
        except (KeyboardInterrupt, EOFError):
            print('')
            return 'exit'

    def run(self):
        for cmd in self.bot.walk_commands():
            print(cmd)
        while self.get_command() != 'exit':
            try:
                self.send_message(self.command)
            except CommandError as ex:
                print(ex)

    def setup(self, config):
        result_msg = 'Pseudo Bot started!\nExtensions:'
        for extension in config.data.extensions:
            if extension.startswith('addons'):
                continue
            result = "Success"
            try:
                self.loader.load_extension(extension)
            except ExtensionError as exception:
                result = str(exception)
            result_msg += f'\n - {extension}: {result}'
        print(result_msg)

    def start(self):
        config = YAMLConfigReader(defaults={
            'prefix': '!',
            'playing': None,
            'extensions': []
        })
        self.setup(config)
        self.run()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('botdir', help='Directory of bot')
    return parser.parse_args()

def main():
    args = parse_args()
    try:
        os.symlink(args.botdir, 'extensions')
        YAMLConfigReader.default_file = os.path.join(args.botdir, 'config.yml')
        BotCli().start()
    finally:
        os.unlink('extensions')
        os.unlink('./administration.yml')

if __name__ == '__main__':
    main()
