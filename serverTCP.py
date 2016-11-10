import select
import socket
import threading



def talk(ear, address):
    print("Nouvelle connexion acceptee de "+str(address))
    while True:
        data = ear.recv(1500)
        if len(data) == 0: # Si la longueur recue est 0 c'est que l'user s'est deconnecte
            print("Client deconnecte")
            break
        print("Message de "+str(address)+":" + data)
        ear.send(data)

    ear.close()
    print("Fermeture de le connexion avec "+str(address))



def main():

    # creation du socket
    ear = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    ear.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    ear.bind(('',7777))
    ear.listen(5)
    print("Serveur lance")
    # Boucle d'attente de connexion
    print("Attente de connexion...")
    
    while True:
        stream = ear.accept()
        threading.Thread(None, talk, None, (stream[0], stream[1],)).start()




    pass


main()
