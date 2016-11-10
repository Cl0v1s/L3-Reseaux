import select
import socket
import threading


def main():

    # creation du socket
    ear = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, 0)
    ear.bind(('',7777))
    print("Serveur lance")
    # Boucle d'attente de connexion
    while True:
        data = ear.recvfrom(1500)
        print("Nouvelle connexion "+str(data[1]))
        print("Message: "+data[0])
        ear.sendto(data[0], data[1])




    pass


main()
