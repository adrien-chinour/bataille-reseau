#!/usr/bin/python3

from game import *
from reseau import *
import  random
import time
import sys

""" generate a random valid configuration """
def randomConfiguration():
    boats = [];
    while not isValidConfiguration(boats):
        boats=[]
        for i in range(5):
            x = random.randint(1,10)
            y = random.randint(1,10)
            isHorizontal = random.randint(0,1) == 0
            boats = boats + [Boat(x,y,LENGTHS_REQUIRED[i],isHorizontal)]
    return boats

def sendGame(game, player, socket):
    otherPlayer = (player+1)%2
    data = getConfiguration(game.boats[player], game.shots[otherPlayer], showBoats=True)
    data = data + getConfiguration([], game.shots[player], showBoats=False)
    socket.send(data)

def getConfiguration(boats, shots=[], showBoats=True):
    Matrix = [[" " for x in range(WIDTH)] for y in range(WIDTH)]

    if showBoats:
        for i in range(NB_BOATS):
            b = boats[i]
            (w,h) = boat2rec(b)
            for dx in range(w):
                for dy in range(h):
                    Matrix[b.x+dx-1][b.y+dy-1] = str(i)
    for (x,y,stike) in shots:
        if stike:
            Matrix[x-1][y-1] = "X"
        else:
            Matrix[x-1][y-1] = "O"
    l = ""
    for y in range(WIDTH):
        for x in range(WIDTH):
            l = l + str(Matrix[x][y])
    return l

""" display the game viewer by the player"""
def displayGame(data):
    for k in range(0,2):
        for i in range(0, WIDTH+1):
            l = ""
            if i == 0:
                l = "  "
            else:
                l = l + chr(ord("A")+i-1) + " "
            for j in range(1, WIDTH+1):
                if i == 0:
                    l = l + str(j) + " "
                else:
                    l = l + data[(i-1)*10+j-1+k*100] + " "
            print(l)
        print("======================")


""" Play a new random shot """
def randomNewShot(shots):
    (x,y) = (random.randint(1,10), random.randint(1,10))
    while not isANewShot(x,y,shots):
        (x,y) = (random.randint(1,10), random.randint(1,10))
    return (x,y)


def main():
    
    if(len(sys.argv) ==1):
        #creation serveur
        server = createServer()
        l = [server]
        while(1):
            a,_,_ = select.select(l,[],[])
            for so in a:
                if(so==server):
                    nc,_ = server.accept()
                    l.append(nc)
                    nc.send("cc\n".encode())
                else:
                    m = so.recv(1500)
                    print(data.decode())
                    if(len(m)==0):
                        so.close
                        l.remove(so)
    else:
        #creation client
        client = createClient(sys.argv[1],sys.argv[2])
        l = [client]
        while(1):
            a,_,_ = select.select(l,[],[])
            for so in a:
                m = so.recv(1500)
                print(m.decode())
                if(len(m)==0):
                    so.close
                    l.remove(so)



    """
    boats1 = randomConfiguration()
    boats2 = randomConfiguration()
    game = Game(boats1, boats2)
    displayGame(game, 0)
    print("======================")

    currentPlayer = 0
    displayGame(game, currentPlayer)
    while gameOver(game) == -1:
        print("======================")
        if currentPlayer == J0:
            x_char = input ("quelle colonne ? ")
            x_char.capitalize()
            x = ord(x_char)-ord("A")+1
            y = int(input ("quelle ligne ? "))
        else:
            (x,y) = randomNewShot(game.shots[currentPlayer])
            time.sleep(1)
        addShot(game, x, y, currentPlayer)
        displayGame(game, 0)
        currentPlayer = (currentPlayer+1)%2
    print("game over")
    print("your grid :")
    displayGame(game, J0)
    print("the other grid :")
    displayGame(game, J1)

    if gameOver(game) == J0:
        print("You win !")
    else:
        print("you loose !")
    """
main()
