import time
from threading import Thread


def initialize(irc, config, job):
    # job = (60, bot.cron)
    channel = config
    print "channel:", channel
    delay = job[0]
    callback = job[1]
    CronJob(irc, channel, delay, callback).start()


class CronJob(Thread):

    def __init__(self, irc, channel, delay, callback):
        Thread.__init__(self)
        self.daemon = True
        self.delay = delay
        self.callback = callback
        self.irc = irc
        self.channel = channel

    def run(self):
        while True:
            time.sleep(self.delay)
            self.irc.send_message(self.channel, self.callback(self.channel))
