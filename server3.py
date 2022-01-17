#!/usr/bin/env python3

from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket 
import time
import os
users = {}
cred = credentials.Certificate('sample-3a85c-firebase-adminsdk-8f6p8-284203a193.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
user_ref = db.collection(u'user')

clients ={}

class Handler(WebSocket):
    def handleMessage(self):
        print("New client has joined")
        

    def handleConncted(self):
        print("bbb")

    def handleClose(self):        
        print("ccc")

server = SimpleWebSocketServer("0.0.0.0",int(os.getenv("PORT",8000)),Handler)
server.serveforever()