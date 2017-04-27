#!/usr/bin/python3

from game import *
from reseau import *
import  random
import time
import sys
import hashlib


# global variable
game = None     #stock la partie en cours
joueur = {}     #dictionnaire des joueurs |clé:numéro du joueur -> (socket,username)
users = {}      #dictionnaire des clients |clé:username -> password
sockuser = {}   #dictionnaire des sockets |clé:socket -> username
nbp = 0         #nombre de joueurs
tour_j = 0      #tour joueur

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
def sendGame(player, socket, turn=False):
    global game
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
def checkGameFinish(l):
    global game, nbp, tour_j
    print("Checking end of game")
    if (gameOver(game) != -1):
        print("Le joueur " + str(gameOver(game)+1) + " à gagné!")
        message = "END" + str(gameOver(game)+1)
        boats1 = randomConfiguration()
        boats2 = randomConfiguration()
        game = Game(boats1, boats2)
        game.shots = [[],[]]
        nbp = 0
        tour_j = 0
        for so in l:
            if so != l[0]:
                so.send(message.encode())
        return True
    return False

""" Play a new random shot """
def randomNewShot(shots):
    (x,y) = (random.randint(1,10), random.randint(1,10))
    while not isANewShot(x,y,shots):
        (x,y) = (random.randint(1,10), random.randint(1,10))
    return (x,y)

""" Permet d'envoyer les configurations a toute les connections """
def sendToAll(sockets, server):
    for so in sockets:
        if so != server:
            if so == joueur[0][0]:
                sendGame(0, joueur[0][0], (tour_j == 0))
            elif so == joueur[1][0]:
                sendGame(1, joueur[1][0], (tour_j == 1))
            else:
                sendGame(-1, so, False)

""" Gestion des messages reçu par le client (protocole personnel) """
def readMessage(m,socket):
    #c'est ton tour! Voici la partie actuelle, tu joue quoi ?
    if(m.startswith('YT')):
        displayGame(m[2:])
        correct = 1
        while correct:
            message = input('Quelles sont les coordonnées à viser ? (ex: B2) \n')
            if((len(message) >= 2) and (len(message)<=3)):
                if((ord(message[1])<=57) and (ord(message[1])>=48)):
                    if((len(message) == 3)and((ord(message[2])<=57)and(ord(message[2])>=48))or(len(message)==2)):
                        if((0<int(message[1:3])) and (int(message[1:3])<=10)):
                            if((0<(ord(message[0].capitalize())-ord("A")+1)) and ((ord(message[0].capitalize())-ord("A")+1)<=10)):
                                correct = 0
        socket.send(('AS'+(format(message))).encode())
    #C'est pas ton tour mais voici l'état de la partie
    elif(m.startswith('WT')):
        displayGame(m[2:])
    elif(m == 'US'):
        username = input('Entrez votre nom d\'utilisateur:\n')
        socket.send(('US'+(format(username))).encode())
    elif(m == 'PW'):
        password = input('Entrez votre mot de passe:\n')
        password = hashlib.sha224(password.encode()).hexdigest()
        socket.send(('PW'+(format(password))).encode())
    elif(m.startswith('END')):
        print("Partie terminé : Le joueur " + m[3:] + " à gagné!")
        message = input('Envie de jouer ? (o/n):\n')
        socket.send(('PLAY'+format(message.capitalize())).encode())
    elif(m.startswith('WC')):
        if(m[2] != "0"):
            num = m[2]
            print("Hey " + m[3:] + "! Tu es le joueur n°" + num + ".")
        else:
            print("Hey " + m[3:] + "! Tu es un observateur.")
    elif(m.startswith('CRT')):
        verifCertif(socket)
        socket.send('OKCRT'.encode())

"""Gestion des messages reçu par le serveur (protocole personnel)"""
def readMessageServer(m,socket,l,server):
    global game, users, joueur, tour_j, nbp, sockuser
    if(m.startswith('US')):
        m = m[2:]
        find = 0
        for user in users:#ajout de preuve de deconnection du joueur //!\\
            if(user == m):
                find = 1
                for key, info_user in joueur.items():
                    if(user == info_user[1]):
                        joueur[key] = (socket,m)
                        break
                sockuser[socket] = m
                break
        if(find == 0):
            sockuser[socket] = m
            users[m] = ('')
        socket.send('PW'.encode())

    elif(m.startswith('PW')):
        m = m[2:]
        print(m)
        if(users[sockuser[socket]] == ''):
            users[sockuser[socket]] = m
            joueur[nbp] = (socket,sockuser[socket])
            nbp+=1
            if(nbp <= 2):
                socket.send(("WC"+str(nbp)+sockuser[socket]).encode())
                # Démarrage de la partie (envoi des configurations initiales)
                if(nbp == 2):
                    sendToAll(l,server)
            else:
                socket.send(("WC0"+sockuser[socket]).encode())
                sendGame(-1, socket, False)
        elif(users[sockuser[socket]] == m):
            for key, info_user in joueur.items():
                if((sockuser[socket] == info_user[1])):
                    joueur[key] = (socket,sockuser[socket])
                    if(key < 2):
                        socket.send(("WC" + str(key+1) + sockuser[socket]).encode())
                    else:
                        socket.send(("WC0" + info_user[1]).encode())
                    if(nbp>=2):
                        if(key < 2):
                            sendGame(key, socket, (tour_j == key))
                        else:
                            sendGame(-1, socket)
                    break
        else:
            socket.send('PW'.encode())

    elif(m.startswith('AS')):
        m = m[2:]
        print(m)
        addShot(game, int(m[1:]), ord(m[0].capitalize())-ord("A")+1, tour_j)
        print("Le joueur " + str(tour_j+1) + " a tiré en " + m)
        if checkGameFinish(l) == False:
            tour_j = (tour_j +1)%2
            sendToAll(l, server)
    elif(m.startswith('PLAY')):
        if m.lstrip('PLAY') == 'O' and nbp < 2:
            joueur[nbp] = (socket,users[sockuser[socket]])
            nbp += 1
            socket.send(("WC"+str(nbp)+sockuser[socket]).encode())
            print(str(nbp))
            if nbp == 2:
                print("restart game")
                sendToAll(l, server)
        else:
            socket.send(("WC0" + sockuser[socket]).encode())
    elif(m.startswith('CRT')):
        f = open(('ca.crt'),'rb')
        l = f.read(4096)
        socket.send(l)
        f.close()
    elif(m.startswith('OKCRT')):
        socket.send('US'.encode())

def main():
    global game
    # Gestion du serveur
    if(len(sys.argv) ==1):
        boats1 = randomConfiguration()
        boats2 = randomConfiguration()
        game = Game(boats1, boats2)
        server = createServer()
        l = [server]
        while(1):
            try:
                a,_,_ = select.select(l,[],[])
            except select.error:
                server.shutdown(2)
                server.close()
                l.remove(server)
                server = createServer()
                l.append(server)
            for so in a:
                # Nouveau socket connecté
                if(so==server):
                    nc,_ = server.accept()
                    l.append(nc)
                    nc.send("CRT".encode())
                else:
                    m = so.recv(1500)
                    m = m.decode()
                    readMessageServer(m,so,l,server)
                    if(len(m)==0):
                        so.close
                        l.remove(so)


    # Gestion d'un client (joueur / observateur)
    else:
        client = createClient(sys.argv[1],sys.argv[2])
        l = [client]
        while(1):
            try:
                a,_,_ = select.select(l,[],[])
            except select.error:
                l.shutdown(2)
                l.close()
                client = createClient(sys.argv[1],sys.argv[2])
                l = [client]
            for so in a:
                m = so.recv(1500)
                if(len(m)==0):
                    so.shutdown(2) #coupe la connexion dans les 2 sens
                    so.close()
                    l.remove(so)
                else:
                    readMessage(m.decode(),so)


main()
