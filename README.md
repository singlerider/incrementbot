Try it out! Code is live at
http://www.twitch.tv/curvyllama
===============================

# Lorenzotherobot

This is a Twitch chat/irc bot written in Python (2.6 / 2.7).

## Installation

Make a copy of the example config file:

`cp src/config/config_example.py src/config/config.py`

#### Globals and Config File

Head into src/config/config.py and enter the correct channels and cron jobs
you'd like to run, then go into globals.py and at the very least replace the
mysql credentials. Leave global_channel, CURRENT_USER, VARIABLE, and
channel_info alone.

## Finally

### To run:

`./serve.py`
