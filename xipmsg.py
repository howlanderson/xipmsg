#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import sys
import string
import protocol
import time
import socket
import os

sys.setcheckinterval(5)

protocol.init()

sys.setcheckinterval(5)

class clientthread(threading.Thread):
    def __init__(self,debug):
        threading.Thread.__init__(self)
        self.debug = debug
    def run(self):
        while True:
            try:
                msg = raw_input()
                msgsquence = msg.strip().split(':')
                print msgsquence
                host = string.join(msgsquence[0], '')
                msg = msgsquence[1:]
                msg = string.join(msg, ':')
                protocol.sendmsg(host, msg)
            except EOFError:
                protocol.logout()
                print "byte byte"
                os.abort()
    
        s.close()

class serverthread(threading.Thread):
    def __init__(self,debug):
        threading.Thread.__init__(self)
        self.debug = debug
    def run(self):
        address = ('', 2425)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(address)

        while True:
            data, (addr, port) = s.recvfrom(2048)

            strlist = data.split(':')
            if strlist[4] == protocol.commandword['IPMSG_SENDMSG'] :
                remotehost = addr
                msg = strlist[5]
                protocol.opthost(strlist[4], remotehost)
                protocol.addcharset(remotehost, protocol.getcharset(msg))
                protocol.printhost()
                protocol.printcharset()
                #print remotehost
                print "<", strlist[2], "><", strlist[3], ">"
                
                print msg.decode(protocol.getcharset(msg))
            elif strlist[4] == protocol.commandword['IPMSG_ANSENTRY'] :
                remotehost = addr
                protocol.optresp('IPMSG_ANSENTRY', remotehost)
            elif strlist[4] == protocol.commandword['IPMSG_BR_EXIT'] :
                remotehost = addr
                protocol.optresp('IPMSG_BR_EXIT', remotehost)

        s.close()

tc = clientthread(1)
ts = serverthread(2)
ts.start()
tc.start()

