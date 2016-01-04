global config

# #### Modify the information in this section
channel = ""  # Leave blank to specify a channel at runtime
username = "YOURUSERNAME"
# get the oauth_password from http://twitchapps.com/tmi/
oauth_password = "oauth:n8urn832r238273nd82"


# #### Do not edit the lines below
channel = "#" + channel.lstrip("#")  # Leave this line alone
if channel == "#":
    channel = "#" + input(
        "No channel specified in config. Which channel would you like to join? "
        ).lstrip("#")

config = {
    # details required to login to twitch IRC server
    'server': 'irc.twitch.tv',
    'port': 6667,
    'username': username,
    'oauth_password': oauth_password,
    'channels': channel,
}
