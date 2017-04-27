from game import *

import socket
import select
import subprocess
import sys,os
import ssl

""" Demarrage du serveur et ecoute sur le port 7777 """
def createServer():
    #partie socket simple
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    #partie initialisation TLS
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain('server.crt','server.key')
    sslconn = context.wrap_socket(s,server_side=True)
    #fin initialisation
    sslconn.bind(('',7777))
    sslconn.listen(1)
    return sslconn

""" Connection du client au serveur """
def createClient(IP,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    #partie initialisation TLS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('ca.crt')
    sslconn = context.wrap_socket(s, server_hostname = IP)
    #fin initialisation
    sslconn.connect((IP, int(float(port))))
    return sslconn
#on peut mettre en commentaire la partie d'initialisation de TLS et modifier
#sslconn en s pour lancer la communication en TCP pour les deux fonctions
    
