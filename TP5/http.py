#!/usr/bin/python3
# coding: utf8

import socket
import sys, traceback


def retrieve(url, page, index=0):
    ip = list()
    try:
        ip = socket.getaddrinfo(url, "www", 0, socket.SOCK_STREAM)
        pipe = socket.socket(ip[index][0], ip[index][1], ip[index][2])
        pipe.connect(ip[index][4])
        data = b"GET "+bytes(page).decode("UTF-8")+b"\r\nHost: "+bytes(url).decode("UTF-8")+b"\r\n"
        print data
        pipe.send(data)

        while 1:
            res = pipe.recv(1024)
            if len(res) == 0:
                break
            print(res)
    except Exception as e:
        if index + 1 >= len(ip):
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print e
            print exc_traceback.tb_lineno
            quit(0)

        retrieve(url,page,  index +1)
    
retrieve(sys.argv[1], sys.argv[2])
