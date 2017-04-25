#!/usr/bin/python3

from game import *
from reseau import *
import  random
import time
import sys

""" generation d'une configuration random """
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

""" Envoi l'état du jeu au joueur sous forme de chaine de caractere de longueur 202 """
""" (2 caractere pour le tour, 100 caractere pour la première config et 100 pour la deuxième) """
def sendGame(game, player, socket, turn):
    print("Envoi des donnees à " + str(player+1))
    if (player != -1):
        otherPlayer = (player+1)%2
        if turn:
            data = "YT"
        else:
            data = "WT"
        data = data + getConfiguration(game.boats[player], game.shots[otherPlayer], showBoats=True)
        data = data + getConfiguration([], game.shots[player], showBoats=False)
        socket.send(data.encode())
    # pour les observateurs
    else:
        data = "WT"
        for i in range(2):
            data = data + getConfiguration(game.boats[i], game.shots[(i+1)%2], showBoats=True)
        socket.send(data.encode())

""" converti la configuration en une chaine de caractère contenant toute les cases de la grille """
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

""" Affiche l'etat de la partie """
def displayGame(data):
    for k in range(2):
        for i in range(WIDTH+1):
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

""" Check if game is over and send data tu player"""
def checkGameFinish(l, game):
    if (gameOver(game) != -1):
        print("Le joueur " + str(gameOver(game)+1) + " à gagné!")
        message = "Le joueur " + str(gameOver(game)+1) + " à gagné!"
        for so in l:
            if so != l[0]:
                so.send(message.encode())

""" Play a new random shot """
def randomNewShot(shots):
    (x,y) = (random.randint(1,10), random.randint(1,10))
    while not isANewShot(x,y,shots):
        (x,y) = (random.randint(1,10), random.randint(1,10))
    return (x,y)

""" Permet d'envoyer les configurations a toute les connections """
def sendToAll(sockets, joueur, game, tour_j, server):
    for so in sockets[1:]:
        if so != server:
            if so == joueur[0]:
                sendGame(game, 0, joueur[0], (tour_j == 0))
            elif so == joueur[1]:
                sendGame(game, 1, joueur[1], (tour_j == 1))
            else:
                sendGame(game, -1, so, False)

""" Gestion des messages reçu par le client (protocole personnel) """
def readMessage(m,socket):

    #c'est ton tour! Voici la partie actuelle, tu joue quoi ?
    if(m.startswith('YT')):
        displayGame(m.lstrip('YT'))
        message = input('Quelles sont les coordonnées à viser ? (ex: B2) \n')
        socket.send((format(message)).encode())

    #C'est pas ton tour mais voici l'état de la partie
    elif(m.startswith('WT')):
        displayGame(m.lstrip('WT'))

    #Je voulais juste te dire que...
    else:
        print(m)

def main():

    # Gestion du serveur
    if(len(sys.argv) ==1):
        boats1 = randomConfiguration()
        boats2 = randomConfiguration()
        game = Game(boats1, boats2)

        server = createServer()
        l = [server]
        joueur = {}
        nbp = 0
        tour_j = 0
        while(1):
            a,_,_ = select.select(l,[],[])
            for so in a:

                # Nouveau socket connecté
                if(so==server):
                    nc,_ = server.accept()
                    l.append(nc)
                    nc.send("Bienvenue\n".encode())
                    joueur[nbp] = nc
                    if(nbp < 2):
                        nc.send(("Vous êtes le joueur " +str(nbp+1)+ "\n").encode())
                        nbp+=1

                        # Démarrage de la partie (envoi des configurations initiales)
                        if(nbp == 2):
                            sendToAll(l, joueur, game, tour_j, server)
                    else:
                        nc.send("Vous êtes un observateur\n".encode())
                        sendGame(game, -1, nc, False)

                # Partie en cours
                elif(nbp >= 2):
                    if(so == joueur[tour_j]):
                        m = so.recv(1500)
                        m = m.decode()
                        print("Le joueur " + str(tour_j+1) + " a tiré en " + m)
                        addShot(game, int(m[1:]), ord(m[0].capitalize())-ord("A")+1, tour_j)
                        checkGameFinish(l, game)
                        if(len(m)==0):
                            so.close
                            l.remove(so)
                        tour_j = (tour_j +1)%2
                        sendToAll(l, joueur, game, tour_j, server)


    # Gestion d'un client (joueur / observateur)
    else:
        client = createClient(sys.argv[1],sys.argv[2])
        l = [client]
        while(1):
            a,_,_ = select.select(l,[],[])
            for so in a:
                m = so.recv(1500)
                if(len(m)==0):
                    so.close
                    l.remove(so)
                else:
                    readMessage(m.decode(),so)

main()
