import select
import socket
import threading


usernames = dict()
channels = list()
channels.append("default")
channels.append("boobs")
locations = dict()


def sendall(clients, channel, sender, message):
    if sender != None: 
        message = usernames[sender] + ": "+message
    else: 
        message = "SERVER: " + message + "\n"
    if message.endswith("\n") == False:
        message = message + "\n"
    print(message)
    for client in clients:
        if client == sender:
            continue
        if channel == None:
            client.send(message)
        elif channel == locations[client]:
            client.send(message)

def send(client, message):
    message = "SERVER: "+message
    if message.endswith("\n") == False:
        message = message + "\n"
    client.send(message)

def close(clients, sender):
    sender.close()
    clients.remove(sender)
    sendall(clients, locations[sender], None,  "PART "+usernames[sender])
    usernames.pop(sender)
    locations.pop(sender)
    print("Client deconnecte")

def switch(clients, client, channel):
    # recuperation de l'ancienne channel
    old = None
    if locations.has_key(client):
        old = locations[client]

    # changement de channel
    locations[client] = channel
    send(client, "========================\nYOU ARE IN CHANNEL "+channel)

    # Envoi des messages aux utilisateurs 
    if old != None: 
        sendall(clients, old, None, "PART "+usernames[client])
    sendall(clients, locations[client], None, "JOIN "+usernames[client])

def kill(clients, client, username):
    for key, value in usernames.items():
        if value == username:
            send(key, "YOU HAVE BEEN KILLED BY "+usernames[client]+"\n")
            sendall(clients,locations[client], None, "KILLED "+value)
            close(clients, key)
            break

def listusers(clients, client):
    message = ""
    for cli in clients:
        message = message + usernames[cli]+", "
    send(client, message)

def nick(clients, client, username):
    for useless, user in usernames.items():
        print(user)
        if user == username:
            send(client, "USERNAME ALREADY EXISTS")
            return
    sendall(clients, locations[client], None, usernames[client] + " IS NOW "+username+"\n")
    usernames[client] = username

def join(clients, client, name):
    if name == locations[client]:
        send(client, "YOU ALREADY ARE IN THE REQUESTED CHANNEL")
        return
    find = False
    for channel in range(0, len(channels)):
        if channels[channel] == name:
            find = True
            switch(clients, client, channels[channel])
            break
    if find == False:
        send(client, "REQUESTED CHANNEL DOES NOT EXISTS")

def kick(clients, client, username):
    for key, value in usernames.items():
        if value == username:
            if locations[key] == channels[0]: # si le mec est deja sur le canal par defaut, on le kill
                kill(clients, client, username)
                return
            # Sinon on le remet sur le canal par defaut
            send(key, "YOU HAVE BEEN KICKED BY "+usernames[client]+"\n")
            sendall(clients,locations[client], None, "KICKED "+value)
            switch(clients, client, channels[0])
            break

def main():

    clients = list()
    # creation du socket d'ecoute
    ear = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    ear.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    ear.bind(('',7777))
    ear.listen(1)
    print("Serveur lance")
    # Boucle d'attente de connexion
    print("Attente de connexion...")
    while True:
        tmp = list(clients)
        tmp.append(ear)
        changes = select.select(tmp, list(), list())[0]
        for client in changes:
            if client == ear: # Si c'est le socket d'ecoute qui vient d'etre modifie, on accpete la connexion
                data = client.accept()
                print("Nouvelle connexion de "+str(data[1]))
                clients.append(data[0])
                usernames[data[0]] = data[1][0]
                switch(clients, data[0], channels[0])
                
            else: # Sinon c'est qu'on vient de recevoir des donness

                data = client.recv(1500)

                # gestion de la deconnexion
                if len(data) == 0: # Si la longueur recue est 0 c'est que l'user s'est deconnecte
                    close(clients, client)

                # Analyse du paquet
                if data.startswith("NICK "):
                    data = data.replace("NICK ", "").replace("\n", "")
                    nick(clients, client, data)
                elif data.startswith("LIST"):
                    listusers(clients, client)
                elif data.startswith("KILL"):
                    data = data.replace("KILL ", "").replace("\n", "")
                    kill(clients, client, data)
                elif data.startswith("MSG "):
                    data = data.replace("MSG", "").replace("\n", "") 
                    sendall(clients, locations[client], client, data)
                elif data.startswith("JOIN "):
                    data = data.replace("JOIN ", "").replace("\n", "")
                    join(clients, client, data)

                elif data.startswith("KICK "):
                    data = data.replace("KICK ", "").replace("\n", "")
                    kick(clients, client, data)



                    

                
    pass


main()
