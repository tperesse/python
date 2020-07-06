#!/usr/bin/python3
# coding: utf8

# import os

# counter = [1, 2]
# # while True:



# def get_creds(useranme):
#     with open('creds.txt') as f:
#         for x in f:
#             credential = x.strip().split(' ', 1)
#             user, passwd = credential[0], credential[1]
#             if user == msg:
#                 return user, passwd
#             continue

# username, password = get_creds(msg)
# print(username, password)

    # def check_username(username, counter):
    #     if username == "none" or len(counter) > 3:
    #         if len(counter) != 0:
    #             del counter[0]
    #         else:
    #             os._exit(1)
    #         print("BYE")
    #     else:
    #         if msg == username:
    #             print("WELC")

# def check_username(username, counter):
#     # Si le mdp est égale à rien.
#     if len(counter) > 0:
#         if username == "none":
#             # Si la liste n'est pas vide on retire un. 
#             del counter[0]
#             return "BYE"
#         else:
#             if msg == username:
#                 return "WELC"
#             else:
#                 del counter[0]
#                 return "BYE"
#     else:
#         return "BYE"

# def check_password(password, counter):
#     # Si le mdp est égale à rien.
#     if len(counter) > 0:
#         if password == "none":
#             # Si la liste n'est pas vide on retire un. 
#             del counter[0]
#             return "BYE"
#         else:
#             if msg_2 == password:
#                 return "WELC"
#                 os._exit(1)
#             else:
#                 del counter[0]
#                 return "BYE"
#     else:
#         return "BYE"

# def get_creds(useranme):
#     with open('creds.txt') as f:
#         for x in f:
#             credential = x.strip().split(' ', 1)
#             user, passwd = credential[0], credential[1]
#             if user == useranme:
#                 return user, passwd
#             continue

# username, password = get_creds(msg)

# def check_creds(username, password, reponse):
#     if password == "none" or username == "none":
#         return "BYE"
#     else:
#         if username in reponse:
#             if password in reponse:
#                 return "WELC"
#             else:
#                 return "BYE"
#         else:
#             return "BYE" 

# for _ in range(3):
#     username = input("user: ")
#     password = input("password: ")
#     compare = ['theo', '123']
#     lol = check_creds(username, password, compare)
#     if lol == "WELC":
#         print("WELC")
#         break
#     print("BYE")

import os
import sys
import socket
import signal

def socket_serveur(sock):
    try:
        sock.bind(('127.0.0.1', 15000))
        sock.listen(1)
        print("En attente de client")
    except socket.error as msg:
            print("Erreur :",msg)
            sys.exit()

def connexion_client():
    connexion, adresse = sock.accept()
    print("Le client avec le socket "+str(adresse[1])+" est connecté")
    msg_bonj = connexion.recv(1024)
    print(msg_bonj.decode())
    ask_passd(connexion)
    # while True:
    #     message = connexion.recv(1024).decode()
    #     print('\n'+ message)


def get_creds(username):
    with open('creds.txt') as f:
        for x in f:
            credential = x.strip().split(' ', 1)
            user, passwd = credential[0], credential[1]
            if user == username:
                return user, passwd
            continue

def check_creds(username, password, reponse):
    if password == "None" or username == "None" or reponse == "None":
        return "BYE"
    else:
        try:
            if username in reponse:
                if password in reponse:
                    return "WELC"
                else:
                    return "BYE"
            else:
                return "BYE" 
        except TypeError:
            return "BYE"

def ask_passd(connfd):
# On demande son username et on cherche ses infos d'authent dans le fichier.
    msg_who = "WHO"
    msg_who = msg_who.encode()
    connfd.send(msg_who)
    for _ in range(3):
        asw_who = connfd.recv(1024).decode()
        user_passwd = get_creds(asw_who)
        # On demande son password.
        msg_passwd = "PASSWD"
        msg_passwd = msg_passwd.encode()
        connfd.send(msg_passwd)
        asw_passwd = connfd.recv(1024).decode()
        # On compare ce que le client a envoyé avec les creds du fichier.
        compare_creds = check_creds(asw_who, asw_passwd, user_passwd)
        if compare_creds == "WELC":
            msg_welc = "WELC"
            msg_welc = msg_welc.encode()
            connfd.send(msg_welc)
            break
        # Envoie du message "BYE".
        msg_bye = "BYE"
        msg_bye = msg_bye.encode()
        connfd.send(msg_bye)

if __name__ == "__main__": 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_serveur(sock)
    connexion_client()

# def msg_who(connfd):
#     msg_who = "WHO"
#     msg_who = msg_who.encode()
#     connfd.send(msg_who)

# def msg_passwd(connfd):
#     msg_passwd = "PASSWD"
#     msg_passwd = msg_passwd.encode()
#     connfd.send(msg_passwd)