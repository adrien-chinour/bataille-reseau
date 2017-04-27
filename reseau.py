from game import *

import socket
import select
import subprocess
import sys,os

""" Demarrage du serveur et ecoute sur le port 7777 """
def createServer():
    s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #au cas ou des connection serait encore en cours sur le port
    s.bind(('',7777))
    s.listen(1)
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
    tree = b''
    #cmdexist = ['if', '[','-f','"server.key"', ']',';','then','echo','"ok"',';','fi']
    #p = subprocess.Popen(cmdexist, stdout=subprocess.PIPE)
    if(not os.path.isfile('server.key')):
        cmd = ['certtool','--generate-privkey','--outfile', 'server.key']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    #for line in p.stdout:
    #    tree+=line
    #print(tree.decode())
    #p.wait()
    #print(p.returncode)

def verifCertif(socket):# le client récupère un certificat
    if(not os.path.isfile('ca.crt')):
        socket.send('CRT'.encode())
        f = open('ca.crt','wb')
        l = socket.recv(1024)
        while(l):
            f.write(l)
            l = socket.recv(1024)
        f.close()
    print('ok certif\n')
