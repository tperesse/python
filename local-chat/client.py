#!/usr/bin/python3
# coding: utf8

import socket, threading, os, sys

def socket_client(SOCK):
# Cette fonction sert à initialiser la connexion du client
# au serveur.

    # Lancement d'un "try" pour la tentative de connexion.
    try:
        SOCK.connect(('127.0.0.1', 12809))
        # Affichage d'un message en cas de réussite.
        print('connexion au serveur réussi...')
        print("Tapez 'FIN' pour sortir du chat.")
    except socket.error:
        # Affichage d'un message en cas d'erreur.
        print("la connexion a échoué.......")
        # Le script se stop.
        sys.exit()


def envoi(utilisateur):
# Cette fonction se chargera de l'envoie au serveur des messages
# écrit par le client.

    try:
        while True:
            msg = input('vous > ')
            message = utilisateur+' > '+msg
            # Encodage du message, nécessaire pour pouvoir l'envoyer au serveur.
            message = message.encode()
            SOCK.send(message)
            # Lancement d'un "try" pour mettre fin au script.
            if msg == "FIN":
                return
    # On catch l'erreur lorsque la connexion est coupée.
    except socket.error:
        print('Le petit chat est mort.')

def reception():
# Cette fonction se chargera de la réception et de l'affichage des messages
# (écrit par les clients) et envoyés par le serveur.

    while True:
        # Réception et décodage des messages.
        message = SOCK.recv(1024).decode()
        # S'il n'y a pas de message on sort de la boucle pour éviter les boucle inf.
        if not message:
            return
        # Affichage des messages.
        print('\n'+ message + '\nvous > ', end='')

if __name__ == "__main__":
# Cette condition correspond à notre main(). Il contient les threads des fonctions 
# "envoie" et "reception". Ainsi que des variables utilisées en paramètre.

    # Contruction du socket client en TCP.
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Appel de la fonction pour qu'elle est en argument le constructeur et 
    # ainsi lancer le socket.
    socket_client(SOCK)
    # Variable contenant les noms des utilisateurs.
    UTILISATEUR = input("Entrer votre nom pour entrer dans le chat > ")
    # Lancement du thread de la fonction "envoie" avec en paramètre un liste contenant les 
    # noms des utilisatuers.
    THREAD_ENVOI= threading.Thread(target=envoi, args=[UTILISATEUR])
    THREAD_ENVOI.start()
    # Lancement du thread de la fonction "réception".
    THREAD_RECEPTION = threading.Thread(target=reception, daemon=True)
    THREAD_RECEPTION.start()