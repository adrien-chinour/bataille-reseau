from game import *

import socket
import select


""" Demarrage du serveur et ecoute sur le port 7777 """
def createServer():
    s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(('',7777))
    s.listen(1)
    return s

""" Connection du client au serveur """
def createClient(IP,port):
    s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,0)
    s.connect((IP,int(float(port))))
    """ Note : pour une connection en local a la place de IP metre '' (bug chez moi) """
    return s
