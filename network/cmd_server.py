#!/usr/bin/python
# coding: utf-8

import socket
import cmd

class MyCmd(cmd.Cmd):

    def help_hello(self):
        print 'say hello'
    def do_hello(self, hoge):
        print 'Hello, world %s san' % hoge

    def help_EOF(self):
        print 'Quit the program'
    def do_EOF(self, line):
        sys.exit()

stHost = socket.gethostbyname("localhost")
inPort = 10000


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

while True:
    stMsg = client_sock.recv(1024)
    if stMsg == "":
         client_sock.send("server : connection end \n\n")
         break

    for i in range(len(stMsg)):
        print("[Client] %x" % ord(stMsg[i]) )
    stRes = p.onecmd(stMsg)
    client_sock.send("[Server]: %s ¥n" % stRes)

client_sock.close()
sock.close()
