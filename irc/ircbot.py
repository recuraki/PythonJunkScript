#!env python


import irc.client
import sys


class IRCCat(irc.client.SimpleIRCClient):
    def __init__(self, target):
        irc.client.SimpleIRCClient.__init__(self)
        self.target = target

    def on_welcome(self, connection, event):
        # after connect
        if irc.client.is_channel(self.target):
            connection.join(self.target)

    def on_join(self, connection, event):
        # after connect
        pass

    def on_disconnect(self, connection, event):
        sys.exit(0)

    def on_pubmsg(self, c, e):
        nick = irc.client.NickMask(e.source).nick
        message = e.arguments[0]
        entry = "({0:>10s}) {1}".format(nick, message)
        print entry
        self.connection.privmsg(self.target, message)

reactor = irc.client.Reactor()

if __name__ == "__main__":
    c = IRCCat("#tech")
    try:
        c.connect("45.0.129.232", 6667, "kanai-bot2", "interop2015")
    except irc.client.ServerConnectionError as x:
        print(x)
        sys.exit(1)
    c.start()
