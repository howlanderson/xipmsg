#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import time
import getpass
import struct
import string


s = ''
commandword = {'IPMSG_NOOPERATION':'0','IPMSG_BR_ENTRY':'1','IPMSG_BR_EXIT':'2','IPMSG_ANSENTRY':'3','IPMSG_SENDMSG':'32','IPMSG_RECVMSG':'33'}

hostlist = []
charsetlist= [None] * 1024
		
def init():
    msgnum = str(int(time.time()))
    protocolversion = '1'
    sender = getpass.getuser()
    hostname = socket.gethostname()
    commandkey = commandword['IPMSG_NOOPERATION']
    print protocolversion , ':' , msgnum , ':' , sender , ':' , hostname , ':' , commandkey , ':'
    msg = protocolversion + ':' + msgnum + ':' + sender + ':' + hostname + ':' + commandkey + ':'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
    s.sendto(msg, ('255.255.255.255', 2425))
    
    msgnum = str(int(time.time()))
    commandkey = commandword['IPMSG_BR_ENTRY']
    print protocolversion , ':' , msgnum , ':' , sender , ':' , hostname , ':' , commandkey , ':'
    msg = protocolversion + ':' + msgnum + ':' + sender + ':' + hostname + ':' + commandkey + ':'
    s.sendto(msg, ('255.255.255.255', 2425))
    s.close()
    
def logout():
    msgnum = str(int(time.time()))
    protocolversion = '1'
    sender = getpass.getuser()
    hostname = socket.gethostname()
    commandkey = commandword['IPMSG_BR_EXIT']
    print protocolversion , ':' , msgnum , ':' , sender , ':' , hostname , ':' , commandkey , ':'
    msg = protocolversion + ':' + msgnum + ':' + sender + ':' + hostname + ':' + commandkey + ':'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
    s.sendto(msg, ('255.255.255.255', 2425))
    s.close()
    
def sendmsg(host, msg):
    msgnum = str(int(time.time()))
    protocolversion = '1'
    sender = getpass.getuser()
    hostname = socket.gethostname()
    commandkey = commandword['IPMSG_SENDMSG']
    if host in hostlist :
        index = hostlist.index(host)
        charset = charsetlist[index]
        print charset
        msg = msg.encode(charset)
    else :
        print "sendmsg error"
    print protocolversion , ':' , msgnum , ':' , sender , ':' , hostname , ':' , commandkey , ':', msg
    msg = protocolversion + ':' + msgnum + ':' + sender + ':' + hostname + ':' + commandkey + ':' + msg
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
    s.sendto(msg, (host, 2425))
    s.close()
    
def addhost(host):
    if host not in hostlist:
        hostlist.append(host)
    
def delhost(host):
    if host in hostlist:
        hostlist.remove(host)
        
def opthost(command, host):
    if command == commandword['IPMSG_ANSENTRY'] :
        addhost(host)
    elif command == commandword['IPMSG_BR_EXIT'] :
        delhost(host)
    elif command == commandword['IPMSG_SENDMSG'] :
        addhost(host)

def getcharset(str):
    try:
        str.decode('utf8')
        return 'utf8'
    except:
        pass
    try:
        str.decode('gbk')
        return 'gbk'
    except:
        pass
        return 'unicode'

def addcharset(hostname, charset):
    if hostname in hostlist:
        index = hostlist.index(hostname)
        charsetlist[index] = charset
    else :
        addhost(hostname)
        index = hostlist.index(hostname)
        charsetlist[index] = charset

def printhost():
    for index, host in enumerate(hostlist):
        print index, ":", host
def printcharset():
    for index, charset in enumerate(charsetlist):
        if charset is None :
            pass
        else :
            print index, ":", charset
