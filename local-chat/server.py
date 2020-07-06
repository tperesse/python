#!/usr/bin/python3
# coding: utf8

import socket, threading

DEBUG = False

def debug(msg):
    """Fonction de debug, affiche les messages si DEBUG est à True."""
    if DEBUG:
        print(msg)


def info(msg):
    """Fonction qui permet d'afficher les messages quand tout va bien. """
    print(msg)


def socket_serveur(sock):
    # Cette fonction sert à initialiser les paramètres du serveur
    # et de lancer l'écoute du socket.

    sock.bind(('127.0.0.1', 12809))
    # Le serveur ne pourra dialoguer qu'avec 5 clients. 
    sock.listen(5)
    info('Le chat est lance sur le port : 12809')


def connexion_client():
    # Cette fonction aura pour but d'accepter les connexions
    # venant des clients, et de lancer en thread la fonction
    # handler. De cette façon le script acceptera les connexions et en
    # parallèle il "broacastera" les messages.

    while True:
        debug('prêt à recevoir une nouvelle connexion')
        connexion, adresse = SOCK.accept()
        debug('connexion acceptée')
        LISTE_DE_CONNEXIONS.append(connexion)
        info("Le client avec le socket "+str(adresse[1])+" est connecté")
        thread_client = threading.Thread(target=handler, args=[connexion])
        thread_client.start()

def handler(connexion):
    # Cette fonction enverra tous les messages des clients au autre sauf à lui-même.

    debug('Ouverture de la connexion %s' % str(connexion))
    # On essaye d'envoyer le message.
    try:
        # Permet de traiter le connexion qui a été envoyée en paramètre.
        with connexion:
            while True:
                message = connexion.recv(1024)
                # Si la connexion meurt cela evite une boucle inf et sort de la boucle.
                if not message:
                    debug('Connexion morte')
                    return
                decoded = message.decode()
                debug('!!!' + decoded + ' (longueur=%d)' % len(decoded))
                # client contiendra le contenu de la liste "liste_de_connexions".
                for client in LISTE_DE_CONNEXIONS:
                    # Si le contenu de la liste ne correspond pas à la liste passé en paramètre,
                    # on envoie le message.
                    if client != connexion:
                        client.send(message)
                # sortir si FIN reçu
                if decoded.endswith('> FIN'):
                    debug('Fermeture de la connexion %s.' % str(connexion))
                    return
    # On catch l'erreur.
    except:
        debug('Je meurs')
        input('pause!')
    # Peu importe le résultat on supprime la connexion avec le client pour éviter loop inf.
    finally:
        debug('Retrait de la connexion')
        LISTE_DE_CONNEXIONS.remove(connexion)


if __name__ == "__main__":
    # Cette condition correspond à notre main(), il contient deux variables qui sont
    # utilisées dans les différentes fonctions. Il est plus pratique de ne pas les mettre
    # à l'intérieur d'une fonction pour éviter les appels de fonctions superflues. 
    # Il contient également le thread de la fonction "connexion_client".
 
    LISTE_DE_CONNEXIONS = []
    # Construction du socket pour des connexions en TCP.
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Appel de la fonction pour qu'elle est en argument le constructeur et 
    # ainsi lancer le socket.
    socket_serveur(SOCK)
    info('Ready.')
    # Lancement du thread de la fonction connexion_client. 
    THREAD_CONNEXION_CLIENT = threading.Thread(target=connexion_client)
    THREAD_CONNEXION_CLIENT.start()
