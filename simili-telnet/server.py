#!/usr/bin/python3.5
from __future__ import print_function
import os
import sys
import socket
import signal

# def socket_serveur(sock):
#     try:
#         sock.bind(('127.0.0.1', 15000))
#         sock.listen(1)
#         print("En attente de client")
#     except socket.error as msg:
#             print("Erreur :",msg)
#             sys.exit()

# def connexion_client():
#     connexion, adresse = sock.accept()
#     print("Le client avec le socket "+str(adresse[1])+" est connecté")
#     ask_passd(connexion)
#     # while True:
#     #     message = connexion.recv(1024).decode()
#     #     print('\n'+ message)

# if __name__ == "__main__": 
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     socket_serveur(sock)
#     connexion_client()

def get_creds(reponse):
    with open('creds.txt') as f:
        for x in f:
            credential = x.strip().split(' ', 1)
            user, passwd = credential[0], credential[1]
            if user == reponse:
                return passwd
            continue

def check_creds(password, reponse):
    if password == "None" or reponse == "None":
        return "BYE"
    else:
        try:
            if password == reponse:
                return "WELC"
            else:
                return "BYE" 
        except TypeError:
            return "BYE"

def ask_passd(connfd):
    print("1")
    for _ in range(3):
        print("2")
        # Demande du username.
        msg_who = "WHO"
        msg_who = msg_who.encode()
        connfd.send(msg_who)
        asw_who = connfd.recv(1024).decode()
        print("WHO:", asw_who)

        # On récupère le mdp en fonction du username du fichier.
        user_passwd = get_creds(asw_who)

        # On demande son password.
        msg_passwd = "PASSWD"
        msg_passwd = msg_passwd.encode()
        connfd.send(msg_passwd)
        asw_passwd = connfd.recv(1024).decode()
        print("PASSWD:", asw_passwd)

        # On compare ce que le client a envoyé avec les creds du fichier.
        compare_creds = check_creds(asw_passwd, user_passwd)

        # On envoie "WELC" au client.
        if compare_creds == "WELC":
            msg_welc = "WELC"
            msg_welc = msg_welc.encode()
            connfd.send(msg_welc)
            break

        # Envoie du message "BYE".
        msg_bye = "BYE"
        msg_bye = msg_bye.encode()
        connfd.send(msg_bye)
        print("3")
    print("4")

def serveur_fils(connfd):
    # sockfd.close()
    msg_bonj = connfd.recv(1024)
    print(msg_bonj.decode())
    ask_passd(connfd)
    while True:
        recu = connfd.recv(1024)
        if len(recu) == 0:
            print("Deconnexion de",client)
            connfd.close()
            sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : ",sys.argv[0],"n°_port")
        sys.exit()

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sockfd.bind(('', int(sys.argv[1])))
    except socket.error as msg:
        print("Erreur :", msg)
        sys.exit()

    sockfd.listen(10)
    print("Attente d'un client")
    while True:
        connfd, client = sockfd.accept()
        print("Connexion de", client)   
        child = os.fork()
        if child == 0:
            serveur_fils(connfd)
        else:
            connfd.close()