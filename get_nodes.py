import socket
import json
import config
import random
import os
import time

def get_nodes(obj, data):
    with open("nodes.db", 'rb') as file:
        while True:
            data = file.read(100)
            if not data:
                break
            obj.send(data)

def send(god=False):
    if god:
        nodes = config.brokers
    else:
        nodes = config.nodes.find("nodes", {"relay":1})
        random.shuffle(nodes)
    for x in nodes:
        s = socket.socket()
        try:
            s.connect((x['ip'], x['port']))
        except:
            s.close()
            continue
        else:
            s.send(json.dumps({"cmd":"get_version"}))
            data = s.recv(1024)
            if data == config.version:
                s.close()
                s = socket.socket()
                try:
                    s.connect((x['ip'], x['port']))
                except:
                    s.close()
                    continue
                else:
                    s.send(json.dumps({"cmd":"get_nodes"}))
                    out = ""
                    while True:
                        data = s.recv(1024)
                        if not data:
                            break
                        out = out + data
                    while os.path.exists("nodes.lock"):
                        time.sleep(0.1)
                    open("nodes.lock", 'w').close()
                    with open("nodes.db", 'wb') as file:
                        file.write(out)
                    os.remove("nodes.lock")
                    break
            else:
                s.close()

