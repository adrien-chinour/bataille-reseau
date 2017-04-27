from game import *

import socket
import select
import subprocess
import sys,os
import ssl

""" Demarrage du serveur et ecoute sur le port 7777 """
def createServer():
    #partie socket TCP
    s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    #partie initialisation TLS
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain('server.crt','server.key')
    sslconn = context.wrap_socket(s,server_side=True)
    sslconn.bind(('',7777))
    sslconn.listen(1)
    #socket.close()
    #createKeyServer()
    #createAutorite()
    return sslconn




""" Connection du client au serveur """
def createClient(IP,port):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('ca.crt')
    s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,0)
    sslconn = context.wrap_socket(s, server_hostname = IP)
    sslconn.connect((IP, int(float(port))))
    return sslconn

    
