#!/usr/bin/python
# coding: utf-8

import socket
import cmd

class InputBuffer(object):
    stBuffer = ""
    def __init__(self, p, sock):
        self.p = p
        self.sock = sock

    def input_char(self, chInput):

        #if ord(chInput) < int("0x20", 16) or ord(chInput) > int("0x7f", 16):
        #   return
        if ord(chInput) == int("0x00", 16):
            return
        if ord(chInput) == int("0x0d", 16):
            print("enter")
            self.run()
            self.stBuffer = ""
            return
        print("[Client] %d" % ord(chInput) )
        self.stBuffer = self.stBuffer + chInput
        #self.sock.send(chInput)

    def run(self):
        stRes = self.p.onecmd(self.stBuffer)
        if stRes != None:
            self.sock.send("[Server]: %s\r\n" % stRes)


class MyCmd(cmd.Cmd):

    def help_hello(self):
        return('say hello')
    def do_hello(self, hoge):
        return('Hello, world %s san' % hoge)

    def help_EOF(self):
        return('Quit the program')
    def do_EOF(self, line):
        sys.exit()

stHost = socket.gethostbyname("localhost")
inPort = 10000
stBuffer = ""


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((stHost, inPort))
sock.listen(1)

print("listen...")

(client_sock, client_addr) = sock.accept()

client_sock.send("server : connection start \n\n")
stRemoteAddr, inRemotePort = client_addr

# IAC WONT LINEMODE IAC WILL ECHO
client_sock.send("\377\375\042\377\373\001");

p = MyCmd(stdin = client_sock)
p.prompt = 'My Prompt: '

InputBuffer = InputBuffer(p, client_sock)

while True:
    stMsg = client_sock.recv(1024)
    if stMsg == "":
         client_sock.send("server : connection end \n\n")
         break

    for i in range(len(stMsg)):
        InputBuffer.input_char(stMsg[i])

client_sock.close()
sock.close()
