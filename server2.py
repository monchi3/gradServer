#!/usr/bin/env python3

from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
from websocket_server import WebsocketServer
import time
import os
users = {}
cred = credentials.Certificate(
    'sample-3a85c-firebase-adminsdk-8f6p8-284203a193.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
user_ref = db.collection(u'user')


def start():

    def new_client(client, server):
        print('New client {}:{} has joined.'.format(
            client['address'][0], client['address'][1]))
        print(client['id'])
        server.send_message(client, 'login')
        global users
        users[client['id']] = {"state": 0,
                               "ID": client['id'], "userID": "", "isAdmin": False, "connection": client}

    def client_left(client, server):
        global users
        global clients
        for user in users.values():
            if user["isAdmin"] == True:
                server.send_message(user["connection"],"1"+","+users[client['id']]["userID"]+",,,,,,,")
        
        #print('Client {}:{} has left.'.format(
        #    client['address'][0], client['address'][1]))
        #users.pop(client['id'])

        #print(client['address'], "closed")

    def message_received(client, server, message):
        global users
        global clients
        print("received" +message)
        if users[client['id']]["state"] == 0:  # ログイン前
            hoge = user_ref.where(u'id', u'==', message)
            docs = hoge.stream()
            for doc in docs:  # ユーザのIDがデータベースのものと一致するか確認
                print(doc.to_dict()["id"])
                if doc.to_dict()["id"] == message:  # 一致するならstateを1に
                    print(client['address'], "join", message)
                    if doc.to_dict()["isAdmin"] == True:  # ユーザがアドミンか確認
                        users[client['id']]["isAdmin"] = True
                        server.send_message(client, "this id is admin")
                    else:
                        server.send_message(client, "this id is exist")
                     # ログイン成功メッセージを返す
                    users[client['id']]["userID"] = message
                    users[client['id']]["state"] = 1
                    break
            if users[client['id']]["state"] == 0:  # idが存在しなかったらエラーメッセージを返す
                # 一致しないならエラーメッセージを返す
                print("this id is not exist")
                server.send_message(client, "this id is not exist")

        elif users[client['id']]["state"] == 1:
            if users[client['id']]["isAdmin"] == True:  # ユーザがアドミンかどうか確認
                print("aaa")
                a = 1
            else:
                for user in users.values():
                    if user["isAdmin"] == True:
                        print("send"+message)
                        server.send_message(user["connection"], message)
                # アドミンでないならアドミンに送信

    server = WebsocketServer(port=int(os.getenv('PORT', 8000)), host='0.0.0.0')
    # イベントで使うメソッドの設定

    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    # 実行
    server.run_forever()


if __name__ == "__main__":
    start()
