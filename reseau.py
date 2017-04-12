from game import *

import socket
import select

def sendGame(game, player, socket):
    otherPlayer = (player+1)%2
    data = getConfiguration(game.boats[player], game.shots[otherPlayer], showBoats=True)
    data = data + getConfiguration([], game.shots[player], showBoats=False)
    socket.send(data)
