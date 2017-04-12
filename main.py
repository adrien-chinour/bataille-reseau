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


def getConfiguration(boats, shots=[], showBoats=True):
    Matrix = [["N" for x in range(WIDTH)] for y in range(WIDTH)]

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
    otherPlayer = (player+1)%2
    getConfiguration(game.boats[player], game.shots[otherPlayer], showBoats=True)
    getConfiguration([], game.shots[player], showBoats=False)

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
        joueur = {}
        nbp = 1 #nb de participants
        tour_j = 0
        while(1):
            a,_,_ = select.select(l,[],[])
            for so in a:
                if(so==server):
                    nc,_ = server.accept()
                    l.append(nc)
                    nc.send("Bienvenue\n".encode())
                    joueur[nbp] = nc
                    if(nbp < 3):
                        nc.send(("Vous êtes le joueur " +str(nbp)+ "\n").encode())
                        nbp+=1
                    else:
                        nc.send("Vous êtes un observateur\n".encode())
                        nbp+=1
                else:
                    if(so == joueur[tour_j+1]):
                        m = so.recv(1500)
                        print(m.decode())
                        if(len(m)==0):
                            so.close
                            l.remove(so)
                        tour_j = (tour_j +1)%2
                    else:
                        m = so.recv(1500)
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
            message = input('enter \n')
            so.send((format(message)).encode())
            print("aaaa\n")
            
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
