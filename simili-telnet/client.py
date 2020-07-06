#!/usr/bin/python3

from __future__ import print_function
import os
import sys
import socket
import select

# def comm_to_server(sock):
#     msg_bonj = "BONJ"
#     msg_bonj = msg_bonj.encode()
#     sock.send(msg_bonj)
#     while True:
#         recu = sock.recv(1024).decode()
#         print(recu, end='\n')
#         msg = input('')
#         msg = msg.encode()
#         sock.send(msg)

# if __name__ == "__main__":
#     # Création du socket.
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect(('127.0.0.1', 15000))
#     # La source de données est un fichier.
#     comm_to_server(sock)

def client(end_data, connectes, sockfd):
    # J' envoie "BONJ" au serveur
    msg_bonj = "BONJ"
    msg_bonj = msg_bonj.encode()
    sockfd.send(msg_bonj)
    while True:
        # Je récupère ce que le serveur envoie et je l'affiche.
        msg = sockfd.recv(1024).decode()
        print(msg)
        a_lire, [], [] = select.select(connectes,[],[])
        for desc in a_lire:
            print("2")
            # On surveille que le serveur est toujours dispo.
            if desc == sockfd:
                recu = sockfd.recv(1024).decode()
                if len(recu) != 0:
                    print("3")
                    print(recu)
                    continue
                    # recu=str(recu,'latin')
                else:
                    if end_data == 0:
                        print("Deconnexion du serveur")
                        sys.exit(-1)
                    else:
                        sys.exit(0)
            # On lit le "stdin" et on envoie au serveur
            if desc == fd:
                print("4")
                lu = os.read(fd, 1024).decode().strip('\n').encode()
                if len(lu) == 0:
                    sockfd.shutdown(socket.SHUT_WR)
                    end_data = 1
                    connectes = [sockfd]
                else:
                    sockfd.send(lu)

if __name__ == "__main__":
    if sys.argv[3] != "stdin":
        fd = os.open(sys.argv[3],os.O_RDONLY)
    else:
        fd = sys.stdin.fileno()

    connectes = [fd]
    end_data = 0
    sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sockfd.connect((sys.argv[1], int(sys.argv[2])))
    connectes.append(sockfd)
    client(end_data, connectes, sockfd)