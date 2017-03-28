# -*- coding: utf-8 -*-
import socket
import select
import threading

PORT = 7777

def initServer():
    s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(('',PORT))
    s.listen(1)
    return s

def initClient(ip, port):
    s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,0)
    s.connect((ip,int(port)))
    s.bind(('',7778))
    s.listen(1)
    return s
    
def sendMessage(struc,lod,so,serveur):
    for i in lod:
        if i!=serveur and i!=so:
            i.send(struc)


def readMessage(struc,l,so, s):
    if(struc.startswith("MSG")):
        if(struc.startswith("MSG public") and public[so]):
            sendMessage(struc,public,so)
        elif(struc.startswith("MSG canal1") and canal1[so]):
            sendMessage(struc,canal1,so)
        elif(struc.startswith("MSG canal2") and canal2[so]):
            sendMessage(struc,canal2,so)         
    elif struc.startswith("NICK"):
        users[so] = struc.strip("NICK \n")
    elif struc.startswith("LIST"):
        for conn in users:
            conn = users[conn] + "\n"
            so.send(conn)
    elif struc.startswith("KILL"):
           user = struc.strip("KILL \n")
           for sk,v in users.items():    
               if v == user:
                   sk.send("BOUH\n")
                   sk.close
                   del users[sk]
                   l.remove(sk)
    elif struc.startswith("JOIN"):
        if struc.startswith("JOIN public"):
            public[so]=1
            #sendMessage(struc,public,so)
        elif struc.startswith("JOIN canal1"):
            canal1[so]=1
            #sendMessage(struc,canal1,so)
        elif struc.startswith("JOIN canal2"):
            canal2[so]=1
            #sendMessage(struc,canal2,so)
    elif struc.startswith("PART"):
        if struc.startswith("PART public"):
            public[so]=0
            #sendMessage(struc,public,so)
        elif struc.startswith("PART canal1"):
            canal1[so]=0
            #sendMessage(struc,canal1,so)
        elif struc.startswith("PART canal2"):
            canal2[so]=0
            #sendMessage(struc,canal2,so)
    elif struc.startswith("KICK"):
        if struc.startswith("KICK public"):
            user = struc.strip("KICK public \n")
            for sk,v in users.items():    
                if v == user:
                    public[sk]=0
            #sendMessage(struc,public,so)
        elif struc.startswith("KICK canal1"):
            user = struc.strip("KICK canal1 \n")
            for sk,v in users.items():    
                if v == user:
                    public[sk]=0
            #sendMessage(struc,canal1,so)
        elif struc.startswith("KICK canal2"):
            user = struc.strip("KICK canal2 \n")
            for sk,v in users.items():    
                if v == user:
                    canal2[sk]=0
            #sendMessage(struc,canal2,so)
