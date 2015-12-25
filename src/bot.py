"""
incrementor for words in a Twitch chat
"""

import lib.irc as irc_
import sys
import datetime
import traceback
import sched
import time
import threading
import os
import curses
import src.config.config as config

channel = config.channel
print channel
word = raw_input("What's the word we're counting here? ")
initial_count = raw_input("What number are we starting at? ")
with open("increment.txt", "w") as f:  # save current date when app starts
    f.write(initial_count)

class Roboraj(object):

    def __init__(self, config):
        self.config = config
        self.irc = irc_.irc(config)

    def run(self):

        def increment():
            with open("increment.txt", "r") as f:
                count = int(f.read())
            with open("increment.txt", "w") as f:
                f.write(str(count + 1))
            return count + 1

        config = self.config

        stdscr = curses.initscr()
        curses.cbreak()
        stdscr.keypad(1)
        stdscr.addstr(0, 10, "Hit 'spacebar' to increment or 'q' to quit")
        stdscr.refresh()
        key = ''
        while key != ord('q'):
            key = stdscr.getch()
            if key == ord(" "):
                count = increment()
                resp = "{0} count: {1}".format(word, count)
                self.irc.send_message(channel, resp)
                stdscr.refresh()

        curses.endwin()
