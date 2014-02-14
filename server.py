import socket
import os
import pickle
from threading import Thread
from Player import Player
from Connecting import Connecting
from AI import Clock

os.system("title Server")


HOST = "localhost"
PORT = 34860

SHUTDOWN_RESTART = ""

while True:
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST,PORT))
    
    # "Users" contains all users playing by using a dictionary system where the
    # key is the User's address and the value is their player object.
    USERS = {}
    ADMINS = {}
    
    # CONNECTING is a dictionary of all users who are in the process of
    # connecting to the server where the key is their address and the value is
    # the Connecting object.
    CONNECTING = {}    
    
    # This lets one IP address run multiple clients
    ALLOW_MULTIPLE_CONNECTIONS = False
    
    # Start game clock
    GAMECLOCK = Clock()
    GAMECLOCK.start()
    
    # Build the interface so commands can be run from the server window.
    class Injection(Thread):
        def __init__(self):
            Thread.__init__(self)
            
        def run(self):
            while True:
                try:
                    command = input()
                    exec(command)
                except Exception as errorMSG:
                    print(errorMSG)   
                print()
    Injector = Injection()
    Injector.start()
    
    while True:
        print()
        data, address = s.recvfrom(1024)
        data = data.decode("utf-8")
        
        # RESPONSE will contain the string to be sent to the address.
        RESPONSE = ""
        
        if data == "DISCONNECT":
            if address in USERS:
                print("User", USERS[address], "disconnecting at:", address)
                del USERS[address]
            elif address in ADMINS:
                print("Admin", ADMINS[address], "disconnecting at:", address)
                del ADMINS[address]
        
        elif address in USERS:
            RESPONSE = USERS[address].interpret(data)
            
            print("Sender:", USERS[address], "at", address)
            print("Received:", data)
            print("Replying with:", RESPONSE)
                    
        elif address in CONNECTING:
            if CONNECTING[address].get_status() == "UNKNOWN":
                if data.lower() == "load":
                    CONNECTING[address].set_status("LOAD")
                    RESPONSE = ("Okay.\nWhat is your username?")
                elif data.lower() == "new":
                    CONNECTING[address].set_status("NEW")
                    RESPONSE = ("Okay.\nWhat would you like your username to be?")
                else:
                    RESPONSE = ("I didn't catch that.\nType 'load' or 'new' to proceed.")
                    
            elif CONNECTING[address].get_status() == "LOAD":
                RESPONSE = CONNECTING[address].load(data)
                
            elif CONNECTING[address].get_status() == "NEW":
                RESPONSE = CONNECTING[address].new(data)
            
            if CONNECTING[address].get_status() == "CONNECTED":
                USERS[address] = CONNECTING[address].generate()
                print("User", str(USERS[address]), "has joined at", address)
                del CONNECTING[address]
                
        elif data == "CONNECT":
            print("Client attempting to connect at:", address)
            if address in USERS and not ALLOW_MULTIPLE_CONNECTIONS:
                print("!!! This client is attempting to connect multiple times.")
                RESPONSE = ("You are already connected.")
            else:
                CONNECTING[address] = Connecting(address)
                RESPONSE = ("Welcome to the server!\nType 'load' or 'new' to proceed.")

        
        # Admin cases below which probably won't be used much longer.
        elif data == "ADMIN LOGIN 42":
            print("^^^ Admin connecting at:", address)
            
            ADMINS[address] = Player("Admin " + str(len(ADMINS)+1))
            
            RESPONSE = ("Welcome, admin!")
            
        elif address in ADMINS:
            if data == "SHUTDOWN":
                RESPONSE = ("Shutting down server!")
                print("^^^ Shutting down!")
                SHUTDOWN_RESTART = "SHUTDOWN"
                break
            elif data == "RESTART":
                RESPONSE = ("Restarting server!")
                print("^^^ Restarting!")
                SHUTDOWN_RESTART = "RESTART"
                break            
            print(">>> Executing adminitrator command:", data)
            try:
                exec(data)
                RESPONSE =("It has been done.")
                print(">>> SUCCESS")
            except Exception as errorMSG:
                RESPONSE =("Erm... That didn't go as planned:\n"+str(errorMSG))
                print(">>> FAILURE")
                
        else:
            print("!!! Something fishy coming from", address)
            print("!!! They sent:", data)
            RESPONSE = ("Modded Client? Want the ban hammer?")
        
        # RESPOND
        s.sendto(bytes(RESPONSE, "utf-8"), address)
    
    s.close()
    
    if SHUTDOWN_RESTART == "SHUTDOWN":
        break