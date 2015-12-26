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
import json

words = {}
keys = {}
channel = config.channel
print channel  # channel connecting to


def add_word():
    word = '{0}'.format(raw_input("What's the word we're counting here? "))
    try:
        initial_count = str(int(raw_input("What number are we starting at? ")))
    except:
        initial_count = "0"
    words[word] = initial_count
    with open("words.json", "w") as f:  # save current date when app starts
        f.write(json.dumps(words))
    n = 0
    while True:
        try:
            if word[n] not in keys:
                keys[word[n].lower()] = word
                print keys
                break
            if word[n] in keys:
                n += 1
                continue
        except Exception as error:
            print "That didn't work. I can't find a unique key from '{0}' that hasn't been used.".format(word)
            break
    continue_adding = raw_input("Would you like to add another word? (y/N) ")
    if "y" in continue_adding.lower():
        print "words", words
        add_word()
    with open("keys.json", "w") as f:
        f.write(json.dumps(keys))

use_previous = raw_input("Would you like to use the last set of counts? (y/N) ")
if "y" in use_previous.lower():
    try:
        with open("words.json", "r") as f:
            words = json.loads(f.read())
        with open("keys.json", "r") as f:
            keys = json.loads(f.read())
    except:
        words = {}
        keys = {}
        print "No previous counts found. Starting a new count:"
        add_word()
else:
    add_word()


class Roboraj(object):

    def __init__(self, config):
        self.config = config
        self.irc = irc_.irc(config)
        incoming_data.initialize(self.irc, self.config.get('channels', {}))

    def run(self):

        def increment(word, count):
            with open("words.json", "r") as f:
                count = int(json.loads(f.read())[word])
            with open("words.json", "w") as f:
                words[word] = count + 1
                f.write(json.dumps(words))
            return count

        def get_greeting(words):
            word_list = "\n" + "\n".join(["Press \"" + str(
                key) + "\" to increment " + str(
                keys[key]) + ". Current count: " + str(
                words[keys[key]]) for key in keys])
            greeting = """Hit 'escape' to quit.\n
                            {0}""".format(word_list)
            return greeting

        config = self.config

        def initiate_screen(words):
            screen = curses.initscr()
            curses.noecho()
            curses.curs_set(0)
            screen.keypad(1)
            screen.addstr(get_greeting(words))
            return screen

        screen = initiate_screen(words)
        key = ''
        while True:
            event = screen.getch()
            if event == 27:
                curses.endwin()
                sys.exit()
            elif chr(event) in keys:
                event = chr(event)
                if keys[event] in words:
                    word = keys[event]
                    count = words[word]
                    screen.clear()
                    count = increment(word, count)
                    screen.addstr(get_greeting(words))
                    resp = "{0} count: {1}".format(word, count + 1)
                    self.irc.send_message(channel, resp)
