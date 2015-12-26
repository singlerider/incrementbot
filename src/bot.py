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


# A recursive function to add a word to the dict of words to be counted
def add_word():
    word = '{0}'.format(raw_input("What's the word we're counting here? "))
    try:
        initial_count = str(int(raw_input("What number are we starting at? ")))
    except:
        initial_count = "0"
    words[word] = initial_count  # word: number {"AI": 2, "pmc": "7"}
    with open("words.json", "w") as f:  # save words json file
        f.write(json.dumps(words))
    # the below loop ensures only unique keys are entered from a word
    n = 0  # initiate an incrementor
    while True:
        try:
            if word[n].lower() not in keys:  # uses incrementor to check letter
                keys[word[n].lower()] = word  # {"a": "AI", "p": "pmc"}
                print {word[n].lower(): {word: initial_count}}
                break  # escape the while loop
            if word[n] in keys:
                n += 1  # try the next letter if the previous is used
                continue  # go back to the beginning of the loop
        except Exception as error:  # happens without unique characters
            print "That didn't work. I can't find a unique key from '{0}' that hasn't been used.".format(word)
            break  # escape the while loop
    continue_adding = raw_input("Would you like to add another word? (y/N) ")
    if "y" in continue_adding.lower():  # "yes"/"Yeah"/"y"
        add_word()  # add words
    with open("keys.json", "w") as f:  # open keys.json
        f.write(json.dumps(keys))  # write converted dict to file as json

# use_previous will decide if the previous count will be used
use_previous = raw_input("Would you like to use the last used counts? (y/N) ")
if "y" in use_previous.lower():  # "yes"/"Yeah"/"y"
    try:
        with open("words.json", "r") as f:  # read words.json
            words = json.loads(f.read())  # get json and convert to dict
        with open("keys.json", "r") as f:  # read keys.json
            keys = json.loads(f.read())  # get json and convert to dict
    except:  # happens if there is no previous counts files
        words = {}  # reset words dict
        keys = {}  # reset keys dict
        print "No previous counts found. Starting a new count:"
        add_word()  # run the function to add words due to failure
else:  # if it's not decided to reuse the previous count
    add_word()  # add words


class Roboraj(object):

    def __init__(self, config):
        self.config = config  # use config.py as this instance's config
        self.irc = irc_.irc(config)  # use irc.py for socket connections
        # asyncronously check for incoming PINGs and send PONGs to server
        incoming_data.initialize(self.irc, self.config.get('channels', {}))

    def run(self):

        def increment(word, count):  # increase the count for a word by one
            with open("words.json", "r") as f:  # read words.json
                count = int(json.loads(f.read())[word])  # use int from json
            with open("words.json", "w") as f:  # open words.json
                words[word] = count + 1  # increase count by one
                f.write(json.dumps(words))  # write complete words dict to file
            return count

        def get_greeting(words):  # what will be displayed on screen
            # list comprehension of all words and current counts
            word_list = "\n" + "\n".join(["Press \"" + str(
                key) + "\" to increment " + str(
                keys[key]) + ". Current count: " + str(
                words[keys[key]]) for key in keys])
            greeting = "Hit 'escape' to quit.\n{0}".format(word_list)
            return greeting

        def initiate_screen(words):  # set up curses "window"
            screen = curses.initscr()  # initiates window
            curses.noecho()  # standard default settings
            curses.curs_set(0)
            screen.keypad(1)
            screen.addstr(get_greeting(words))  # display greeting
            return screen

        screen = initiate_screen(words)  # set screen as variable
        key = ""  # initiate key as an empty string
        while True:  # main event loop
            event = screen.getch()  # key that gets pressed
            if event == 27:  # translation of "ESC" key to ord
                curses.endwin()  # terminate window
                sys.exit()  # cleanly close program
            elif chr(event) in keys:  # convert keypress to chr str
                event = chr(event)  # ensure event is a converted keypress str
                if keys[event] in words:  # if the keypress is a match
                    word = keys[event]  # {event: word}
                    count = words[word]  # {word: count}
                    screen.clear()  # clear screen of previous count
                    count = increment(word, count)  # add one to count
                    screen.addstr(get_greeting(words))  # display new greeting
                    resp = "{0} count: {1}".format(word, count + 1)
                    # submit corresponding word and count to stream chat
                    self.irc.send_message(channel, resp)
