#!/usr/bin/python3

"""
Ce script a pour but de simuler un serveur pour le projet simili-telnet.
Fait par :
- Théo PERESSE
- Alexandre KOSTAS
- Jean-Alexandre PIOT
- Philippe DA SILVA OLIVEIRA
"""

import os
import sys
import socket
import select
import pty
import time

def ls(path):
    """Fonction permettant de lister le contenu du dossier qui nous est donné en paramètre."""
    try:
        # On ouvre le fichier en écriture.
        fd = os.open("ls.txt", os.O_WRONLY | os.O_CREAT)
        # On efface le contenu du fichier avant d'y inscrire de nouvelles choses.
        os.ftruncate(fd, 0)
        # os.dup2 va nous permettre de rediriger dans "fd" ce que affiche os.execlp.
        os.dup2(fd, pty.STDOUT_FILENO)
        os.execlp("/bin/ls", 'ls', path)
        # On quitte la fonction.
        sys.exit(0)
    except OSError:
        print("erreur d'ouverture du fichier ls.txt")
        sys.exit(-1)

def cd(path):
    """Fonction permettant de changer de dossier."""
    # On ouvre le fichier en écriture.
    fd = os.open("cd.txt", os.O_WRONLY | os.O_CREAT)
    # On efface le contenu du fichier avant d'y inscrire de nouvelles choses.
    os.ftruncate(fd, 0)
    # os.dup2 va nous permettre de rediriger dans "fd".
    os.dup2(fd, pty.STDOUT_FILENO)
    # On change de répertoire courant.
    os.chdir(path)
    # On inscrit dans le fichier le contenu du dossier courant.
    os.execlp("/bin/pwd", 'pwd')
    sys.exit(0)

def pwd():
    """Fonction permettant de changer de dossier."""
    try:
        # On ouvre le fichier en écriture.
        fd = os.open("pwd.txt", os.O_WRONLY | os.O_CREAT)
        # On efface le contenu du fichier avant d'y inscrire de nouvelles choses.
        os.ftruncate(fd, 0)
        # os.dup2 va nous permettre de rediriger dans "fd".
        os.dup2(fd, pty.STDOUT_FILENO)
        # On inscrit dans le fichier le contenu du dossier courant.
        os.execlp("/bin/pwd", 'pwd')
        sys.exit(0)
    except OSError:
        print("erreur d'ouverture du fichier ls.txt")
        sys.exit(-1)

def read(file):
    """Fonction permettant de lire et d'envoyer"""
    resultat = []
    # On ouvre le ficher en lecture.
    file = open(file, 'r')
    # On stocke toutes les lignes dans un fichier.
    lines = file.readlines()
    # return lines
    # On fait un 'for' pour lire l'ensemble des lignes et on les envoie au client.
    for line in lines:
        print(line.strip("\n"))
        resultat.append(line.strip("\n"))
    return resultat

def execute_commands(comm, path):
    """Cette fonction permet d'exécuter dans un processus fils la commande passée en paramètre."""
    # Cette commande va permettre de créer un processus fils.
    child = os.fork()
    # En fonction de la variable 'comm' on exécute une certaine commande.
    if comm == "cd" and child == 0:
        cd(path)
    elif comm == "ls" and child == 0:
        ls(path)
    elif comm == "pwd" and child == 0:
        pwd()

def commands(lu):
    """Cette fonction va exécuter le scénario d'utilisation
    des commandes 'ls', 'pwd' et 'cd'."""
    try:
        # Si la commande est "cd" on met à jour la variable.
        if lu == "cd":
            # On supprime l'ancienne valeur de la liste.
            if len(path) != 0:
                del path[0]
            # On demande le dossier où aller et on l'ajoute à la liste
            chemin = input("path > ")
            # On ajoute le chemin dans la vraible path.
            path.append(chemin)
            # On lance la commande 'cd' et on affiche 'CDOK' ou 'NOCD' suivant si ça réussi.
            try:
                execute_commands(lu, path[0])
                time.sleep(3)
                print("CDOK")
            except:
                print("NOCD")
        # Partie qui va lister le contenu du fichier.
        elif lu == "ls":
            # Si 'ls' est la première commande, on va lancer la fonction pwd pour aller chercher
            # le chemin du dossier courant et afficher son contenu.
            if len(path) == 0:
                # On exécute la commande pwd et on l'ajoute à la variable 'path'.
                execute_commands("pwd", " ")
                time.sleep(3)
                pth = read("pwd.txt")
                path.append(pth[0])
                # La variable path etant rempli on peut lancer la fonction ls.
                execute_commands(lu, pth[0])
                time.sleep(3)
                read("ls.txt")
            else:
                # On lance la commande 'ls'.
                execute_commands(lu, path[0])
                time.sleep(3)
                # On affiche le résultat contenu dans un fichier.
                read("ls.txt")
        # Partie qui va afficher le chemin du dossier courant.
        elif lu == "pwd":
            # Si 'pwd' est la première commande, on va lancer la fonction pwd pour aller chercher
            # le chemin du dossier courant et y inscrire le résultat dans la variable 'path'.
            if len(path) == 0:
                execute_commands("pwd", "")
                time.sleep(3)
                pth = read("pwd.txt")
                path.append(pth[0])
            else:
                # Si la commande est 'pwd' on envoie le contenu de la variable 'path'
                # qui correspond au chemin courrant.
                print(path[0])
    except:
        # En cas d'erreur on quitte la fonction.
        return 0

def client(end_data, connectes, sockfd):
    """Fonction permettant de simuler un client."""
    # Envoie "BONJ" au serveur.
    msg_bonj = "BONJ"
    msg_bonj = msg_bonj.encode()
    sockfd.send(msg_bonj)
    while True:
        # On récupère ce que le serveur envoie et on l'affiche.
        msg = sockfd.recv(4096).decode()
        print(msg)
        # Si le message est un "BYE" et qu'il est envoyé 3 fois, on ferme la connexion au serveur.
        if msg == "BYE":
            print("Deconnexion du serveur")
            sys.exit(-1)
        # On se met en attente d'un evenement en lecture sur la socket ou l'entrée de données
        # on recupere dans a_lire le(s) descripteur(s) prêts à lire.
        a_lire, [], [] = select.select(connectes, [], [])
        for desc in a_lire:
            # On surveille que le serveur est toujours disponible sinon on se déconnecte du server.
            if desc == sockfd:
                if end_data == 1:
                    print("Deconnexion du serveur")
                    sys.exit(-1)

            # On lit le "stdin" et on envoie au serveur.
            if desc == fd:
                lu = os.read(fd, 1024).decode().strip('\n').encode()
                # Si on n'a rien lu (EOF).
                if len(lu) == 0:
                    # On ferme la socket en ecriture.
                    sockfd.shutdown(socket.SHUT_WR)
                    # On indique qu'on a fait un shutdown.
                    end_data = 1
                    # On ne surveille plus que la socket.
                    connectes = [sockfd]
                else:
                    comm = lu.decode()
                    if comm == "cd" or comm == "ls" or comm == "pwd":
                        return 0
                    else:
                        # Sinon on envoie dans la socket ce qu'on a lu.
                        sockfd.send(lu)

if __name__ == "__main__":
    """Cette partie correspond au main du programme."""
    # La source de données est un fichier.
    if sys.argv[3] != "stdin":
        # On ouvre le fichier.
        fd = os.open(sys.argv[3], os.O_RDONLY)
    else:
        # La source de donnees est le clavier.
        fd = sys.stdin.fileno()

    # On met le descripteur de l'entree de donnees dans les descripteurs a surveiller
    connectes = [fd]
    # Si end_data=1, c'est qu'on a fait un shutdown sur la socket.
    end_data = 0
    # Création d'un socket actif en TCP.
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connexion au serveur.
    sockfd.connect((sys.argv[1], int(sys.argv[2])))
    # On ajoute le descripteur de socket aux descripteurs à surveiller.
    connectes.append(sockfd)
    # Lancement de la fonction client pour envoyer et recevoir des messages du serveur.
    client(end_data, connectes, sockfd)
    # Partie telnet où on peut exécuter des commandes.
    path = []
    while True:
        lu = input("> ")
        commands(lu)   
