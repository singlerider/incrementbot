# encoding=utf8
import socket
import re
import time
import sys
import _thread
import codecs

threshold = 5 * 60  # five minutes, make this whatever you want


class irc:

    def __init__(self, config):
        self.config = config
        self.ircBuffer = ""
        self.connect()

    def nextMessage(self):
        while "\r\n" not in self.ircBuffer:
            read = self.sock.recv(1024)
            if not read:
                print("Connection was lost")
                self.connect()  # Reconnect.
            else:
                self.ircBuffer += read.decode()
        line, self.ircBuffer = self.ircBuffer.split("\r\n", 1)
        if line.startswith("PING"):
            self.sock.send(str(line.replace("PING", "PONG") + "\r\n").encode())
        return line

    def check_for_message(self, data):
        if re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PRIVMSG #[a-zA-Z0-9_]+ :.+$', data):
            return True

    def check_for_join(self, data):
        if re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) JOIN #[a-zA-Z0-9_]', data):
            return True

    def check_for_part(self, data):
        if re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PART #[a-zA-Z0-9_]', data):
            return True

    def check_is_command(self, message, valid_commands):
        for command in valid_commands:
            if command == message:
                return True

    def check_for_connected(self, data):
        if re.match(r'^:.+ 001 .+ :connected to TMI$', data):
            return True

    def get_logged_in_users(self, data):
        if data.find('353'):
            return True
            #:lorenzotherobot.tmi.twitch.tv 353 lorenzotherobot = #curvyllama :l0rd_bulldog agentsfire workundercover69 the_polite_zombie jalenxweezy13 curvyllama hmichaelh2015 steven0405 armypenguin91 hionas22 prophecymxxm singlerider bentleet tesylesor vipervenom2u zombiesdelux115 lorenzotherobot nerdy0rgyparty michaelcycle gewgled jconnfilm rustemperor frozelio

    def check_for_ping(self, data):
        last_ping = time.time()
        # if data[0:4] == "PING":
        if data.find('PING') != -1:
            self.sock.send(str('PONG ' + data.split()[1] + '\r\n').encode())
            last_ping = time.time()
        if (time.time() - last_ping) > threshold:
            sys.exit()

    def get_message(self, data):
        return re.match(r'^:(?P<username>.*?)!.*?PRIVMSG (?P<channel>.*?) :(?P<message>.*)', data).groupdict()

    def check_login_status(self, data):
        if re.match(r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$', data):
            return False
        else:
            return True

    def send_message(self, channel, message):
        # message can be any of the formats:
        # None - sends nothing
        # String - sends this line as a message
        # List - sends each line individually.
        #  -- technically since this is recursive you can have a tree of messages
        #  -- [["1", ["2", "3"]], "4"] will send "1", "2", "3", "4".
        if not message:
            return
        if isinstance(message, str):
            self.sock.send('PRIVMSG %s :%s\r\n'.encode() % (channel.encode(), message.encode()))
        if type(message) == list:
            for line in message.decode("utf8"):
                self.send_message(channel, line)

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        try:
            print(("Connecting to {}:{}".format(self.config['server'], self.config['port'])))
            sock.connect((self.config['server'], self.config['port']))
        except:
            print(('Cannot connect to server (%s:%s).' %
               (self.config['server'], self.config['port']), 'error'))
            sys.exit()
        sock.settimeout(None)
        sock.send('USER %s\r\n'.encode() % self.config['username'].encode())
        sock.send('PASS %s\r\n'.encode() % self.config['oauth_password'].encode())
        sock.send('NICK %s\r\n'.encode() % self.config['username'].encode())
        self.sock = sock
        loginMsg = self.nextMessage()
        #:tmi.twitch.tv NOTICE * :Login unsuccessful
        # or
        # :tmi.twitch.tv 001 theepicsnail :Welcome, GLHF!
        if "unsuccessful" in loginMsg:
            print("Failed to login. Check your oath_password and username in src/config/config.py")
            sys.exit(1)
        # Wait until we're ready before starting stuff.
        while "376" not in self.nextMessage():
            pass
        self.join_channels(self.channels_to_string(self.config['channels']))

    def channels_to_string(self, channel_list):
        channels = [''.join(channel_list)]
        print(channels)
        return channels

    def join_channels(self, channels):
        print(('Joining channels %s.' % channels[0]))
        self.sock.send('JOIN %s\r\n'.encode() % channels[0].encode())
        print('Joined channels.')

    def leave_channels(self, channels):
        print(('Leaving channels %s,' % channels[0]))
        self.sock.send('PART %s\r\n'.encode() % channels[0].encode())
        print('Left channels.')
