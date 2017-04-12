from game import *

import socket
import select

def createServer():
    s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(('',7777))
    s.listen(1)
    return s

def createClient(IP,port):
    s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,0)
    s.connect((IP,int(float(port))))
    return s
