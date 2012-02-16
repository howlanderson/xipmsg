#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import time
import getpass
import struct
import string

PORT = 2425
PROTOCOL_VERSION = "1"
commandword = {'IPMSG_NOOPERATION':'0','IPMSG_BR_ENTRY':'1','IPMSG_BR_EXIT':'2','IPMSG_ANSENTRY':'3','IPMSG_SENDMSG':'32','IPMSG_RECVMSG':'33','IPMSG_SENDMSG_WITHCHECK':'288'}

hostlist = []
		
def init(socket_handle):
    #print 'protocol init function start'
    msgnum = str(int(time.time()))
    sender = getpass.getuser()
    hostname = socket.gethostname()
    commandkey = commandword['IPMSG_NOOPERATION']
    #print "#init > " , PROTOCOL_VERSION , ':' , msgnum , ':' , sender , ':' , hostname , ':' , commandkey , ':'
    msg = PROTOCOL_VERSION + ':' + msgnum + ':' + sender + ':' + hostname + ':' + commandkey + ':'
    socket_handle.sendto(msg, ('255.255.255.255', 2425))
    
    msgnum = str(int(time.time()))
    commandkey = commandword['IPMSG_BR_ENTRY']
    #print "#init > " , PROTOCOL_VERSION , ':' , msgnum , ':' , sender , ':' , hostname , ':' , commandkey , ':'
    msg = PROTOCOL_VERSION + ':' + msgnum + ':' + sender + ':' + hostname + ':' + commandkey + ':'
    socket_handle.sendto(msg, ('255.255.255.255', 2425))
    while True:
        try:
            data, (addr, port) = socket_handle.recvfrom(1024)
            #print repr(data)
            strlist = data.split(':')
            optresp(strlist[4], addr)
        except socket.timeout:
            break

    #print '#protocol init function stop'
    
def logout():
    msgnum = str(int(time.time()))
    protocolversion = '1'
    sender = getpass.getuser()
    hostname = socket.gethostname()
    commandkey = commandword['IPMSG_BR_EXIT']
    #print "#logout > " , PROTOCOL_VERSION , ':' , msgnum , ':' , sender , ':' , hostname , ':' , commandkey , ':'
    msg = PROTOCOL_VERSION + ':' + msgnum + ':' + sender + ':' + hostname + ':' + commandkey + ':'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
    s.sendto(msg, ('255.255.255.255', 2425))
    s.close()

def sendrecvmsg(client_socket, host, msg):
    msgnum = str(int(time.time()))
    sender = getpass.getuser()
    hostname = socket.gethostname()
    commandkey = commandword['IPMSG_RECVMSG']
    #print "#sendrecvmsg > " , PROTOCOL_VERSION , ':' , msgnum , ':' , sender , ':' , hostname , ':' , commandkey , ':', msg
    msg = PROTOCOL_VERSION + ':' + msgnum + ':' + sender + ':' + hostname + ':' + commandkey + ':' + msg
    client_socket.sendto(msg, (host, PORT))

def sendansentry(client_socket, host):
    msgnum = str(int(time.time()))
    sender = getpass.getuser()
    hostname = socket.gethostname()
    commandkey = commandword['IPMSG_ANSENTRY']
    #print "#sendansentry > " , PROTOCOL_VERSION , ':' , msgnum , ':' , sender , ':' , hostname , ':' , commandkey , ':'
    msg = PROTOCOL_VERSION + ':' + msgnum + ':' + sender + ':' + hostname + ':' + commandkey + ':' 
    client_socket.sendto(msg, (host, PORT))

def sendmsg(client_socket, host, msg):
    msgnum = str(int(time.time()))
    sender = getpass.getuser()
    hostname = socket.gethostname()
    commandkey = commandword['IPMSG_SENDMSG']
    if host in hostlist :
        index = hostlist.index(host)
    else :
        pass
        #print "sendmsg > host not in hostlist"
    #print "#sendmsg > " , PROTOCOL_VERSION , ':' , msgnum , ':' , sender , ':' , hostname , ':' , commandkey , ':', msg
    msg = PROTOCOL_VERSION + ':' + msgnum + ':' + sender + ':' + hostname + ':' + commandkey + ':' + msg
    client_socket.sendto(msg, (host, PORT))
    
def addhost(host):
    if host not in hostlist:
        hostlist.append(host)
    
def delhost(host):
    if host in hostlist:
        hostlist.remove(host)
        
def optresp(command, host):
    if command == commandword['IPMSG_ANSENTRY'] :
        addhost(host)
    elif command == commandword['IPMSG_BR_EXIT'] :
        delhost(host)
    elif command == commandword['IPMSG_SENDMSG'] :
        addhost(host)
    elif command == commandword['IPMSG_BR_ENTRY'] :
        addhost(host)
    else :
        #print '#optresp>invoid resp'
        pass

def printhost():
    for index, host in enumerate(hostlist):
        pass
        #print index, ":", host
