"""
incrementor for words in a Twitch chat
"""

import lib.irc as irc_
import sys
import datetime
import traceback
import sched
import time
import os
import curses
import src.config.config as config
from threading import Thread
from lib.functions_general import *
import src.lib.incoming_data as incoming_data

channel = config.channel
print channel
word = '"{0}"'.format(raw_input("What's the word we're counting here? "))
try:
    initial_count = str(int(raw_input("What number are we starting at? ")))
except:
    initial_count = "0"
with open("increment.txt", "w") as f:  # save current date when app starts
    f.write(initial_count)

class Roboraj(object):

    def __init__(self, config):
        self.config = config
        self.irc = irc_.irc(config)
        incoming_data.initialize(self.irc, self.config.get('channels', {}))

    def run(self):

        def increment():
            with open("increment.txt", "r") as f:
                count = int(f.read())
            with open("increment.txt", "w") as f:
                f.write(str(count + 1))
            return count + 1

        def get_greeting(word, count):
            greeting = "Hit 'spacebar' to increment or 'q' to quit. {0} count: {1}".format(
                word, count)
            return greeting

        config = self.config

        count = initial_count

        def initiate_screen():
            screen = curses.initscr()
            curses.noecho()
            curses.curs_set(0)
            screen.keypad(1)
            screen.addstr(get_greeting(word, count))
            return screen

        screen = initiate_screen()
        key = ''
        while True:
            event = screen.getch()
            if event == ord("q"):
                curses.endwin()
                sys.exit()
            elif event == ord(" "):
                screen.clear()
                count = increment()
                screen.addstr(get_greeting(word, count))
                resp = "{0} count: {1}".format(word, count)
                self.irc.send_message(channel, resp)
