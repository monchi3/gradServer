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





