import socket
import os
from threading import Thread

os.system("title Client")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()

HOST = "localhost"
PORT = 34860
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class Message(Thread):
    def __init__(self):
        Thread.__init__(self)
        
    def run(self):
        while True:
            try:
                data, address = s.recvfrom(1024)
            except:
                continue
            data = data.decode("utf-8")
            
            print(data)
            print()
    
# Send a connect message
s.sendto(bytes("CONNECT", "utf-8"), (HOST,PORT))

messenger = Message()
messenger.start()

while True:
    message = input()
    while message == "":
        print("Well.. say something!")
        message = input(">> ")
        
    clear()
    if message.lower() == "quit":
        s.sendto(bytes("DISCONNECT", "utf-8"), (HOST,PORT))
        break
    else:
        s.sendto(bytes(message, "utf-8"), (HOST,PORT))
    
print()
print("Thanks for playing!")