import socket
from Player import Player
#from AI import Clock

HOST = "localhost"
PORT = 34860

SHUTDOWN_RESTART = ""

while True:
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST,PORT))
    
    # "Users" contains all users playing by using a dictionary system where the key
    # is the User's Address and the value is their player object
    USERS = {}
    ADMINS = {}
    
    CONNECTIONS = 0
    
    # This lets one IP address run multiple clients
    ALLOW_MULTIPLE_CONNECTIONS = True
    
    # Start game clock
    
    #GAMECLOCK = Clock()
    #GAMECLOCK.start()
    
    while True:
        print()
        data, address = s.recvfrom(1024)
        
        data = data.decode("utf-8")
                
        if address in USERS:
            if data == "DISCONNECT":
                print("Client disconnecting at:", address)
                CONNECTIONS -=1
                if address in USERS:
                    del USERS[address]
                continue
            
            reply = USERS[address].interpret(data)
            
            print("Sender:", address)
            print("Received:", data)
            print("Replying with:", reply)
            
            s.sendto(bytes(reply, "utf-8"), address)  
            
        elif data == "CONNECT":
                    print("Client attempting to connect at:", address)
                    if any([key[0] == address[0] for key in USERS.keys()]) and not ALLOW_MULTIPLE_CONNECTIONS:
                        print("!!! This client is attempting to connect multiple times.")
                        s.sendto(bytes("You are already connected.", "utf-8"), address)
                    else:
                        print("Sending initialization data.")
                        
                        CONNECTIONS +=1
                        USERS[address] = Player("Player" + str(CONNECTIONS))
                        
                        s.sendto(bytes("Welcome!", "utf-8"), address)    
            
        elif data == "ADMIN LOGIN 42":
            print("^^^ Admin connecting at:", address)
            
            CONNECTIONS +=1
            ADMINS[address] = Player("Player" + str(CONNECTIONS), [0,0,0])
            
            s.sendto(bytes("Welcome, admin!", "utf-8"), address)  
            
        elif address in ADMINS:
            if data == "SHUTDOWN":
                s.sendto(bytes("Shutting down server!", "utf-8"), address)
                print("^^^ Shutting down!")
                SHUTDOWN_RESTART = "SHUTDOWN"
                break
            elif data == "RESTART":
                s.sendto(bytes("Restarting server!", "utf-8"), address)
                print("^^^ Restarting!")
                SHUTDOWN_RESTART = "RESTART"
                break            
            print(">>> Executing adminitrator command:", data)
            try:
                exec(data)
                s.sendto(bytes("It has been done.", "utf-8"), address)
                print(">>> SUCCESS")
            except Exception as errorMSG:
                s.sendto(bytes("Erm... That didn't go as planned:\n"+str(errorMSG), "utf-8"), address)
                print(">>> FAILURE")
                
        else:
            print("!!! Something fishy coming from", address)
            print("!!! They sent:", data)
            s.sendto(bytes("Modded Client? Want the ban hammer?", "utf-8"), address)
    
    
    s.close()
    
    if SHUTDOWN_RESTART == "SHUTDOWN":
        break
