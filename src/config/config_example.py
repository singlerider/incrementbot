global config

channels_to_join = ['#singlerider']

for channel in channels_to_join:
    channel = channel.lstrip('#')

config = {
    # details required to login to twitch IRC server
    'server': 'irc.twitch.tv',
    'port': 6667,
    'username': 'YOURUSERNAME',
    # get this from http://twitchapps.com/tmi/
    'oauth_password': 'oauth:ksahd7shadiash8dasnd7a',

    'debug': True,
    'log_messages': True,

    'channels': channels_to_join,

}
