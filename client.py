import socket
import os

def clear():
    os.system('cls'  if  os.name==  'nt'  else  'clear')

clear()

HOST = "localhost"
PORT = 34860
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def get_message():
    data, address = s.recvfrom(1024)
    data = data.decode("utf-8")
    
    clear()
    print()
    print(data)
    
# Send a connect message

s.sendto(bytes("CONNECT", "utf-8"), (HOST,PORT))
get_message()

while True:
    message = input(">> ")
    while message == "":
        clear()
        print("Well.. say something!")
        message = input(">> ")
        

    if message.lower() == "quit":
        s.sendto(bytes("DISCONNECT", "utf-8"), (HOST,PORT))
        break
    else:
        s.sendto(bytes(message, "utf-8"), (HOST,PORT))
    
    get_message()
    
print()
print("Thanks for playing!")