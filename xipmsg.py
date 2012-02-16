#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import sys
import string
import protocol
import time
import socket
import os

#init env
sys.setcheckinterval(1)

PORT = protocol.PORT
address = ('', PORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#server_socket.settimeout(1)
server_socket.setblocking(1)
server_socket.bind(address)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_socket.settimeout(1)

#print '#init finished'
protocol.init(client_socket)
#print '#protocol init finished'

print ">"

class clientthread(threading.Thread):
    def __init__(self, client_socket, server_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.server_socket = server_socket
    def run(self):
        while True:
            try:
                msg = raw_input() #get user input
                msgsquence = msg.strip().split(':') #strip the input and explode the string by ":"
                #print msgsquence
                msgsquence2 = msgsquence[0].strip().split('/');
                host = string.join(msgsquence2[1], '')
                msg = msgsquence[1:]
                msg = string.join(msg, ':')
                
                protocol.sendmsg(self.client_socket, host, msg)
                protocol.printhost()
                print ">"

            except EOFError:
                protocol.logout()
                print "byte byte"
                os.abort()
        s.close()

class serverthread(threading.Thread):
    def __init__(self, client_socket, server_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.server_socket = server_socket
    def run(self):
        while True:
            try:
                data, (addr, port) = self.server_socket.recvfrom(1024)
                strlist = data.split(':')
                commandword = strlist[4]
                #print repr(strlist)
                if commandword == protocol.commandword['IPMSG_SENDMSG'] :
                    remotehost = addr
                    msg = strlist[5]
                    protocol.optresp(commandword, remotehost)
                    protocol.printhost()
                    #print '#ipmsg_sendmsg>'
                    print strlist[2],"@",remotehost,">",
                    print msg
                    print ">"
                    #sys.stdout.write(">")
                elif commandword == protocol.commandword['IPMSG_SENDMSG_WITHCHECK'] :
                    msgnum = strlist[1]
                    remotehost = addr
                    protocol.sendrecvmsg(client_socket, remotehost, msgnum) #send msg check

                    msg = strlist[5]
                    protocol.optresp(commandword, remotehost)
                    protocol.printhost()
                    print strlist[2],"@",remotehost,">",
                    print msg
                    print ">"
                elif commandword == protocol.commandword['IPMSG_ANSENTRY'] :
                    remotehost = addr
                    protocol.optresp(protocol.commandword['IPMSG_ANSENTRY'], remotehost)
                elif commandword == protocol.commandword['IPMSG_BR_EXIT'] :
                    remotehost = addr
                    protocol.optresp(protocol.commandword['IPMSG_BR_EXIT'], remotehost)
                elif commandword == protocol.commandword['IPMSG_NOOPERATION'] :
                    #no operation
                    pass
                elif commandword == protocol.commandword['IPMSG_BR_ENTRY'] :
                    remotehost = addr
                    protocol.optresp(protocol.commandword['IPMSG_BR_ENTRY'], remotehost)
                    protocol.sendansentry(client_socket, remotehost)
                elif commandword == protocol.commandword['IPMSG_ANSENTRY'] :
                    remotehost = addr
                    protocol.optresp(protocol.commandword['IPMSG_ANSENTRY'], remotehost)
                else :
                    print "Notice > Uncatched message :",strlist, ":" , commandword
                    print ">"


                protocol.printhost()

            except socket.timeout:
                pass

        s.close()

tc = clientthread(client_socket, server_socket)
ts = serverthread(client_socket, server_socket)
ts.start()
tc.start()
while True:
    try:
        time.sleep(1)
    except EOFError:
        protocol.logout()
        print "byte! byte!"
        os.abort()
