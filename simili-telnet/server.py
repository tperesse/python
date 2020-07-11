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
import signal
import pty
import time

# def rls(path):
#     """Fonction permettant de lister le contenu du dossier qui nous est donné en paramètre."""
#     try:
#         # On ouvre le fichier en écriture.
#         fd = os.open("rls.txt", os.O_WRONLY | os.O_CREAT)
#         # On efface le contenu du fichier avant d'y inscrire de nouvelles choses.
#         os.ftruncate(fd, 0)
#         # os.dup2 va nous permettre de rediriger dans "fd" ce que affiche os.execlp.
#         os.dup2(fd, pty.STDOUT_FILENO)
#         os.execlp("/bin/ls", 'ls', path)
#         # On quitte la fonction.
#         sys.exit(0)
#     except OSError:
#         print("erreur d'ouverture du fichier rls.txt")
#         sys.exit(-1)

# def rcd(path):
#     """Fonction permettant de changer de dossier."""
#     # On ouvre le fichier en écriture.
#     fd = os.open("rcd.txt", os.O_WRONLY | os.O_CREAT)
#     # On efface le contenu du fichier avant d'y inscrire de nouvelles choses.
#     os.ftruncate(fd, 0)
#     # os.dup2 va nous permettre de rediriger dans "fd".
#     os.dup2(fd, pty.STDOUT_FILENO)
#     # On change de répertoire courant.
#     os.chdir(path)
#     # On inscrit dans le fichier le contenu du dossier courant.
#     os.execlp("/bin/pwd", 'pwd')
#     sys.exit(0)

# def read(file, connfd):
#     """Fonction permettant de lire et d'envoyer"""
#     # On ouvre le ficher en lecture.
#     file = open(file, 'r')
#     # On stocke toutes les lignes dans un fichier.
#     lines = file.readlines()
#     # On fait un 'for' pour lire l'ensemble des lignes et on les envoie au client.
#     for line in lines:
#         connfd.send(line.encode())

# def execute_commands(comm, path):
#     """Cette fonction permet d'exécuter dans un processus fils la commande passée en paramètre."""
#     # Cette commande va permettre de créer un processus fils.
#     child = os.fork()
#     # En fonction de la variable 'comm' on exécute une certaine commande.
#     if comm == "rcd" and child == 0:
#         rcd(path)
#     elif comm == "rls" and child == 0:
#         rls(path)

# def commands(connfd):
#     """Cette fonction va exécuter le scénario d'utilisation
#     des commandes 'rls', 'rpwd' et 'rcd'."""
#     # Stockage du chemin.
#     path = []
#     try:
#         # Boucle inf pour jouer plusieurs commandes à la suite.
#         while True:
#             # On demande la commande à exécuter.
#             comm = connfd.recv(1024).decode().strip('\n')
#             msg_path = "PATH"
#             msg_path = msg_path.encode()
#             connfd.send(msg_path)
#             # S'il n'y a rien dans la liste, on lance la commande pour enregistrer un chemin.
#             if len(path) == 0 and comm != "rcd":
#                 chemin = connfd.recv(1024).decode().strip('\n')
#                 path.append(chemin)
#                 execute_commands("rcd", path[0])
#                 # On attend 3 secondes pour laisser le fichier s'update.
#                 time.sleep(3)
#             # Si la commande est "rcd" on met à jour la variable.
#             if comm == "rcd":
#                 # On supprime l'ancienne valeur de la liste.
#                 if len(path) != 0:
#                     del path[0]
#                 # On demande le dossier où aller et on l'ajoute à la liste
#                 chemin = connfd.recv(1024)
#                 path.append(chemin)
#                 # On lance la commande 'rcd'.
#                 try:
#                     execute_commands(comm, path[0])
#                     time.sleep(3)
#                     reponse = "CDOK"
#                     connfd.send(reponse.encode())
#                 except:
#                     reponse = "NOCD"
#                     connfd.send(reponse.encode())
#             elif comm == "rls":
#                 # On lance la commande 'rls'.
#                 execute_commands(comm, path[0])
#                 time.sleep(3)
#                 # On affiche le résultat contenu dans un fichier.
#                 reader = read(comm + ".txt", connfd)
#             elif comm == "rpwd":
#                 # Si la commande est 'rpwd' on envoie le contenu de la variable 'path'
#                 # qui correspond au chemin courrant.
#                 connfd.send(path[0].encode())
#     except:
#         # En cas d'erreur on quitte la fonction.
#         return 0

def rls(path):
    """Fonction permettant de lister le contenu du dossier qui nous est donné en paramètre."""
    try:
        # On ouvre le fichier en écriture.
        fd = os.open("rls.txt", os.O_WRONLY | os.O_CREAT)
        # On efface le contenu du fichier avant d'y inscrire de nouvelles choses.
        os.ftruncate(fd, 0)
        # os.dup2 va nous permettre de rediriger dans "fd" ce que affiche os.execlp.
        os.dup2(fd, pty.STDOUT_FILENO)
        os.execlp("/bin/ls", 'ls', path)
        # On quitte la fonction.
        sys.exit(0)
    except OSError:
        print("erreur d'ouverture du fichier rls.txt")
        sys.exit(-1)

def rcd(path):
    """Fonction permettant de changer de dossier."""
    # On ouvre le fichier en écriture.
    fd = os.open("rcd.txt", os.O_WRONLY | os.O_CREAT)
    # On efface le contenu du fichier avant d'y inscrire de nouvelles choses.
    os.ftruncate(fd, 0)
    # os.dup2 va nous permettre de rediriger dans "fd".
    os.dup2(fd, pty.STDOUT_FILENO)
    # On change de répertoire courant.
    os.chdir(path)
    # On inscrit dans le fichier le contenu du dossier courant.
    os.execlp("/bin/pwd", 'pwd')
    sys.exit(0)

def rpwd():
    """Fonction permettant de changer de dossier."""
    try:
        # On ouvre le fichier en écriture.
        fd = os.open("rpwd.txt", os.O_WRONLY | os.O_CREAT)
        # On efface le contenu du fichier avant d'y inscrire de nouvelles choses.
        os.ftruncate(fd, 0)
        # os.dup2 va nous permettre de rediriger dans "fd".
        os.dup2(fd, pty.STDOUT_FILENO)
        # On inscrit dans le fichier le contenu du dossier courant.
        os.execlp("/bin/pwd", 'pwd')
        sys.exit(0)
    except OSError:
        print("erreur d'ouverture du fichier rpwd.txt")
        sys.exit(-1)

def read(file, connfd):
    """Fonction permettant de lire et d'envoyer"""
    resultat = []
    # On ouvre le ficher en lecture.
    file = open(file, 'r')
    # On stocke toutes les lignes dans un fichier.
    lines = file.readlines()
    # On fait un 'for' pour lire l'ensemble des lignes et on les envoie au client.
    for line in lines:
        connfd.send(line.encode())
        resultat.append(line.strip("\n"))
    return resultat

def execute_commands(comm, path):
    """Cette fonction permet d'exécuter dans un processus fils la commande passée en paramètre."""
    # Cette commande va permettre de créer un processus fils.
    child = os.fork()
    # En fonction de la variable 'comm' on exécute une certaine commande.
    if comm == "rcd" and child == 0:
        rcd(path)
    elif comm == "rls" and child == 0:
        rls(path)
    elif comm == "rpwd" and child == 0:
        rpwd()

def commands(connfd):
    """Cette fonction va exécuter le scénario d'utilisation des commandes 'rls', 'rpwd' et 'rcd'."""
    # Stockage du chemin.
    path = []
    try:
        # Boucle inf pour jouer plusieurs commandes à la suite.
        while True:
            comm = connfd.recv(1024).decode().strip('\n')
            # Si la commande est "rcd" on met à jour la variable.
            if comm == "rcd":
                # On supprime l'ancienne valeur de la liste.
                if len(path) != 0:
                    del path[0]
                msg_path = "PATH"
                msg_path = msg_path.encode()
                connfd.send(msg_path)
                # On demande le dossier où aller et on l'ajoute à la liste
                chemin = connfd.recv(1024)
                path.append(chemin)
                # On lance la commande 'rcd' et on affiche 'CDOK' ou 'NOCD' suivant si ça réussi.
                try:
                    execute_commands(comm, path[0])
                    time.sleep(3)
                    reponse = "CDOK"
                    connfd.send(reponse.encode())
                except:
                    reponse = "NOCD"
                    connfd.send(reponse.encode())
            # Partie qui va lister le contenu du fichier.
            elif comm == "rls":
                # Si 'ls' est la première commande, on va lancer la fonction pwd pour aller chercher
                # le chemin du dossier courant et afficher son contenu.
                if len(path) == 0:
                    # On exécute la commande pwd et on l'ajoute à la variable 'path'.
                    execute_commands("rpwd", " ")
                    time.sleep(3)
                    pth = read("rpwd.txt", connfd)
                    path.append(pth[0])
                    # La variable path etant rempli on peut lancer la fonction ls.
                    execute_commands(comm, path[0])
                    time.sleep(3)
                    read("rls.txt", connfd)
                else:
                    # On lance la commande 'ls'.
                    execute_commands(comm, path[0])
                    time.sleep(3)
                    # On affiche le résultat contenu dans un fichier.
                    reader = read(comm + ".txt", connfd)
            # Partie qui va afficher le chemin du dossier courant.
            elif comm == "rpwd":
                # Si 'pwd' est la première commande, on va lancer la fonction pwd pour aller chercher
                # le chemin du dossier courant et y inscrire le résultat dans la variable 'path'.
                if len(path) == 0:
                    execute_commands("rpwd", "")
                    time.sleep(3)
                    pth = read("rpwd.txt", connfd)
                    path.append(pth[0])
                else:
                    # Si la commande est 'rpwd' on envoie le contenu de la variable 'path'
                    # qui correspond au chemin courrant.
                    pth = read("rcd.txt", connfd)
                    connfd.send(pth[0].encode())
    except:
        # En cas d'erreur on quitte la fonction.
        return 0

def get_creds(reponse):
    """Cette fonction va permettre de récupérer les credentials de l'utilisateur
    depuis le fichier de creds."""
    # Le 'with' va permettre d'ouvrir le fichier puis le refermer à la fin.
    with open('creds.txt') as f:
        for x in f:
            # Pour chaques lignes on supprime et l'espace et on coupe la ligne en deux.
            credential = x.strip().split(' ', 1)
            # On récupère dans 2 variables différentes le username et le password.
            user, passwd = credential[0], credential[1]
            # Si le user passé en paramètre est égal au user du fichiser on retourne le mdp.
            if user == reponse:
                return passwd
            # Si ce n'est pas le cas on continue sur la prochaine itération.
            continue

def check_creds(password, reponse):
    """Fonction qui va retourner 'WELC' ou 'BYE' si les mots de passe sont égaux."""
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
    """Fonction qui va jouer le scnério de l'authentification."""
    for _ in range(3):
        # Demande du username.
        msg_who = "WHO"
        msg_who = msg_who.encode()
        connfd.send(msg_who)
        asw_who = connfd.recv(1024).decode()

        # On récupère le mdp en fonction du username du fichier.
        user_passwd = get_creds(asw_who)

        # On demande son password.
        msg_passwd = "PASSWD"
        msg_passwd = msg_passwd.encode()
        connfd.send(msg_passwd)
        asw_passwd = connfd.recv(1024).decode()

        # On compare ce que le client a envoyé avec les creds du fichier.
        compare_creds = check_creds(asw_passwd, user_passwd)

        # On envoie "WELC" au client et on quitte la fonction.
        if compare_creds == "WELC":
            msg_welc = "WELC"
            msg_welc = msg_welc.encode()
            connfd.send(msg_welc)
            return 0

    # Envoie du message "BYE".
    msg_bye = "BYE"
    msg_bye = msg_bye.encode()
    connfd.send(msg_bye)
    return "BYE"

def serveur_fils(connfd):
    """Fonction qui est lancée comme processus fils et qui va jouer le rôle de serveur."""
    sockfd.close()
    # On affiche le message "BONJ" envoyé par le client.
    msg_bonj = connfd.recv(1024)
    print(msg_bonj.decode())
    # On exécute les différentes commandes pour jouer l'authentification ainsi que les commandes.
    ask_passd(connfd)
    commands(connfd)
    # On lance une boucle infinie pour surveiller le client
    # si plus rien n'est envoyé on ferme la connexion.
    while True:
        recu = connfd.recv(1024)
        if len(recu) == 0:
            print("Deconnexion de", client)
            connfd.close()
            sys.exit(0)

if __name__ == "__main__":
    """Cette partie correspond au main du programme."""
    # On contrôle que que tous les paramètres sont renseignés.
    if len(sys.argv) != 2:
        print("Usage : ", sys.argv[0], "n°_port")
        sys.exit()

    # Le processus ignore le signal SIGCHLD, ainsi les processus fils ne deviendront pas zombies.
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    # Création d'un socket actif en TCP.
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # On lie une IP avec un port.
        sockfd.bind(('', int(sys.argv[1])))
    except socket.error as msg:
        print("Erreur :", msg)
        sys.exit()

    # On laisse la possibilité à 10 clients de se connecter.
    sockfd.listen(10)
    print("Attente d'un client")
    while True:
        # On accepte la demande de connexion du client.
        connfd, client = sockfd.accept()
        print("Connexion de", client)
        # On créé un processus fils pour chaques clients qui se connectent.
        child = os.fork()
        if child == 0:
            serveur_fils(connfd)
        else:
            connfd.close()
