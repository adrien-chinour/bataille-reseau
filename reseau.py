from game import *

import socket
import select
import subprocess
import sys,os

""" Demarrage du serveur et ecoute sur le port 7777 """
def createServer():
    #partie socket TCP
    s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #au cas ou des connection serait encore en cours sur le port
    s.bind(('',7777))
    s.listen(1)
    #partie initialisation TLS
    createKeyServer()
    createAutorite()
    return s

""" Connection du client au serveur """
def createClient(IP,port):
    s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,0)
    s.connect((IP,int(float(port))))
    """ Note : pour une connection en local a la place de IP metre '' (bug chez moi) """
    return s

def sendMessage(sender,recipient,message,IP,port):
    try:
        recipient.send(message)
    except OSError:
        l[0].shutdown(2)
        l[0].close()
        client = createClient(sys.argv[1],sys.argv[2])
        l = [client]

def createAutorite():
    if(not os.path.isfile('ca.key')):
        createKey = ['certtool','--generate-privkey','--outfile', 'ca.key']
        p = subprocess.Popen(createKey, stdout=subprocess.PIPE)
    if(not os.path.isfile('ca.crt')):
        createCertif = ['certtool', '--generate-self-signed', '--template', 'cert.cfg', '--load-privkey', 'ca.key', '--outfile', 'ca.crt']
        p = subprocess.Popen(createCertif, stdout=subprocess.PIPE)

def createKeyServer():
    if(not os.path.isfile('server.key')):
        cmd = ['certtool','--generate-privkey','--outfile', 'server.key']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

def verifCertif(socket):# le client récupère un certificat
    if(not os.path.isfile('ca.crt')):
        socket.send('CRT'.encode())
        f = open('ca.crt','wb')
        l = socket.recv(4096)
        f.write(l)
        f.close()
<<<<<<< HEAD
    print('ok certif\n')
=======
    print('Certificat reçu\n')


    
>>>>>>> d9a36114700d9546f9cd2de0004526cedaa4b84c
