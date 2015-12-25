"""
Intricate Chat Bot for Twitch.tv

By Shane Engelman <me@5h4n3.com>

Contributions from dustinbcox and theepicsnail
"""

import lib.irc as irc_
import sys
import datetime
import traceback
import sched
import time
import threading
import os

END = False


class Roboraj(object):

    def __init__(self, config):
        self.config = config
        self.irc = irc_.irc(config)

    def run(self):

        config = self.config

        while True:
            try:
                data = self.irc.nextMessage()
                if not self.irc.check_for_message(data):
                    continue
                message_dict = self.irc.get_message(data)
                channel = message_dict['channel']
                message = message_dict['message']  # .lower()
                username = message_dict['username']
                part = message.split(' ')[0]
                #valid = False
                #if not valid:
                #    continue
                self.irc.send_message(channel, message)

            except Exception as error:
                print error
