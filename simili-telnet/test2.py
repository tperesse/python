#!/usr/bin/python3
# coding: utf8


# def get_creds(username):
#     with open('creds.txt') as f:
#         for x in f:
#             username = []
#             credential = x.strip().split(' ', 1)
#             user, passwd = credential[0], credential[1]
#             if user == username:
#                 username.append(user)
#                 username.append(passwd)
#                 return username
#             continue

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

username = input("user: ")
password = input("password: ")
print(check_creds(username, password, get_creds(username)))