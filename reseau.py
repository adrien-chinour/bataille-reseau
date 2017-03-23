# -*- coding: utf-8 -*-
import socket
import select
import threading



def create_server():
    s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(('',7777))
    s.listen(1)
    return s

    
def sendmessage(struc,lod,so):
    for i in lod:
        if i!=s and i!=so:
            i.send(struc)


def lecture(struc,l,so):
    #if(struc.startswith("PLAY")):
        
        
    if(struc.startswith("MSG")):
        if(struc.startswith("MSG public") and public[so]):
            sendmessage(struc,public,so)
        elif(struc.startswith("MSG canal1") and canal1[so]):
            sendmessage(struc,canal1,so)
        elif(struc.startswith("MSG canal2") and canal2[so]):
            sendmessage(struc,canal2,so)         
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
            #sendmessage(struc,public,so)
        elif struc.startswith("JOIN canal1"):
            canal1[so]=1
            #sendmessage(struc,canal1,so)
        elif struc.startswith("JOIN canal2"):
            canal2[so]=1
            #sendmessage(struc,canal2,so)
    elif struc.startswith("PART"):
        if struc.startswith("PART public"):
            public[so]=0
            #sendmessage(struc,public,so)
        elif struc.startswith("PART canal1"):
            canal1[so]=0
            #sendmessage(struc,canal1,so)
        elif struc.startswith("PART canal2"):
            canal2[so]=0
            #sendmessage(struc,canal2,so)
    elif struc.startswith("KICK"):
        if struc.startswith("KICK public"):
            user = struc.strip("KICK public \n")
            for sk,v in users.items():    
                if v == user:
                    public[sk]=0
            #sendmessage(struc,public,so)
        elif struc.startswith("KICK canal1"):
            user = struc.strip("KICK canal1 \n")
            for sk,v in users.items():    
                if v == user:
                    public[sk]=0
            #sendmessage(struc,canal1,so)
        elif struc.startswith("KICK canal2"):
            user = struc.strip("KICK canal2 \n")
            for sk,v in users.items():    
                if v == user:
                    canal2[sk]=0
            #sendmessage(struc,canal2,so)




l = [s]
users = {}
public = {}
canal1 = {}
canal2 = {}

while(1):
    a,_,_ = select.select(l,[],[])
    for so in a:
        if(so==s):
            nc,ad = s.accept()
            l.append(nc)
            j = ad[0]
            users[nc]=j
            public[nc]=1
            ad = "JOIN " + j +"\n"
            ad.encode()
            sendmessage(ad,l,so)
        else:
            m = so.recv(1500)
            lecture(m,l,so)
            if(len(m)==0):
                ad = "PART " + users[so] +"\n"
                ad.encode()
                sendmessage(ad,l,so)
                so.close
                del user[so]
                l.remove(so)
