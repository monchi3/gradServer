#!/usr/bin/env python3

from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket 
import time
import os

cred = credentials.Certificate('sample-3a85c-firebase-adminsdk-8f6p8-284203a193.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
user_ref = db.collection(u'user')

users ={}

class Handler(WebSocket):
    def handleConnected(self):
        print("New client has joined")
        global users
        
        users[self.address]={"state":0,"ID":self.address,"userID":"","isAdmin":False,"connection":self}
        
    def handleClose(self):        
        print("Client left")
        global users
        users.pop(self.address)
        
    def handleMessage(self):
        print("message:"+self.data)
        self.sendMessage(self.data)
        print(users)
        
        if(users[self.address]["state"]==0):
            hoge = user_ref.where(u'id',u'==',self.data)
            docs = hoge.stream()
            for doc in docs:
                print(doc.to_dict()["id"])
                if doc.to_dict()["id"] == self.data:
                    print(self.address,"join",self.data)
                    if doc.to_dict()["isAdmin"]==True:
                        users[self.address]["isAdmin"]=True
                        self.sendMessage("this id is admin")
                    else:
                        self.sendMessage("this id is exist")
                    users[self.address]["userID"]=self.data
                    users[self.address]["state"]=1
                    break
            if users[self.address]["state"]==0:
                print("this id is not exist")
                self.sendMessage("this id is not exist")
        elif users[self.address]["state"]==1:
            if users[self.address]["isAdmin"]==True:
                print("aaa")
                a=1
            else:
                for user in users.values():
                    if user["isAdmin"]==True:
                        print("send"+self.data)
                        user["connection"].sendMessage(self.data)
server = SimpleWebSocketServer("0.0.0.0",int(os.getenv("PORT",8000)),Handler)
server.serveforever()