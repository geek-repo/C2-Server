import socket
import threading
from os import system

lis={} #collect connection
ips=[]
count=0
def babies(conn,addr):
    print("[+] Sir you successfully  connected to {}".format(addr))
    conn.sendall(b"suckers")

def start():

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
            count+=1
            lis[addr]=conn
            ips.append(addr)
            print('Connected by', addr)


def client():
    a=1
    if ips:
        for i in ips:
            print ("{} --> {}".format(a,i))
            a+=1
    else:
        print("NO CONNECTION SIRE")

def action():
    e=int(input("Whom you wanna interact with:-"))
    e-=1
    ass=ips[e]

    if ass in lis:
        if lis[ass].recv(1024):
            babies(lis[ass],ass)
        else:
            print("Connection Dead !!")
            del lis[ass]
            ips.remove(ass)



def main():
    system('clear')
    print ("=== Welcome to the server ===")
    threading.Thread(target=start).start()
    print ("[+] Listner Started")
    while True:
        print ("\nPress 1 to view the current asses online\npress 2 to select to interact")
        e=input(">")
        if e=='1':
            p=threading.Thread(target=client)
            p.start()
            p.join()

        elif e=='2':
            p=threading.Thread(target=action)
            p.start()
            p.join()


main()
