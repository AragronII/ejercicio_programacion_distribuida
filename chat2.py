#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:47:07 2023

@author: alumno
"""

from multiprocessing.connection import Client
from random import random
from time import sleep

from multiprocessing import Process
from multiprocessing.connection import Listener

import sys

def client_listener(info):
    print(f"Opening listener at {info}")
    cl = Listener(address=(info['address'], info['port']),\
                  authkey=info['authkey'])
    print('........client listener starting')
    print('........accepting connection')
    while True:
        conn = cl.accept()
        print ('........connection accepted from', cl.last_accepted)
        m = conn.recv()
        print ('........message received from server', m)
        
def main(server_address, info):
    print('trying to connect')
    with Client(address=(server_address, 6000), \
                authkey=b'secret password server') as conn:
        cl = Process(target=client_listener, args=(info,))
        cl.start()
        conn.send(info)
        connected = True
        while connected:
            value = input("Send message ('quit' quit connection)?")
            print ("connection continued...")
            conn.send(value)!='quit'
        cl.terminate()
    print ("end client")
    
if __name__ == '__main__':
    server_address = '127.0.0.1'
    client_address = '127.0.0.1'
    client_port = 6001
    
    if len(sys.argv) > 1:
        client_port = int(sys.argv[1])
    if len(sys.argv) > 2:
        client_address = sys.argv[2]
    if len(sys.argv) > 3:
        client_address = sys.argv[3]
    info = {
        'address': client_address,
        'port': client_port,
        'authkey': b'secret client server'
        }
    main(server_address, info)