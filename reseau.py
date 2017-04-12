from game import *

import socket
import select

def sendGame(game, player, socket):
    otherPlayer = (player+1)%2
    data = getConfiguration(game.boats[player], game.shots[otherPlayer], showBoats=True)
    data = data + getConfiguration([], game.shots[player], showBoats=False)
    socket.send(data)

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
