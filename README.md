# incrementbot

### This is a Twitch chat/irc bot written in Python (3.5.1).

'Ever watch a Twitch stream and think "I wonder how many times they say 'Nanomachines' in Metal Gear Solid 4?"
Well, now you can finally know - and better yet - you can make sure everyone else knows, too!
All it takes is pressing whichever key gets assigned to a particular phrase you enter as you start up the program.

That's it!

![Screencapture GIF](http://i.imgur.com/prY6gqH.gif)

## Installation

Make a copy of the example config file:

`cp src/config/config_example.py src/config/config.py`

### Config File

Head into src/config/config.py and enter the channel you'd like to join and your login credentials.

`channel` is the channel that you would like the bot to join (a Twitch streamer's username).

`username` is your Twitch username!

`oauth_password` is the authentication that Twitch requires to make sure you are who you say you are.
Keep this password secret. It will be formatted similar to `oauth:lh7sandias8nd7as8ndh7ad8s9u`.

You can get your ouath_password at:

http://twitchapps.com/tmi/


### To run:

`./serve.py`
