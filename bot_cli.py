import sys
import os
import argparse

from utils.config_reader import YAMLConfigReader
from pseudo_message import PseudoMessage
from extension_loader import ExtensionLoader
from pseudo_bot import PseudoBot
from discord.ext.commands.errors import *

class BotCli():
    def __init__(self):
        self.bot = PseudoBot()
        self.loader = ExtensionLoader(self.bot)

    def send_message(self, cmd):
        self.bot.run_command(PseudoMessage(cmd))

    def run(self):
        last_command = None
        while last_command != 'exit':
            last_command = input('> ')
            try:
                self.send_message(last_command)
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

    def start(self, config_file):
        config = YAMLConfigReader(defaults={
            'prefix': '!',
            'playing': None,
            'extensions': []
        }, file=config_file)
        self.setup(config)
        self.run()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('botdir', help='Directory of bot')
    return parser.parse_args()

def main():
    args = parse_args()
    sys.path.append(args.botdir)
    BotCli().start(os.path.join(args.botdir, 'config.yml'))
