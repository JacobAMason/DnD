import socket, logging, os
from threading import Thread

os.system("title Client")

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)-15s %(levelname)-8s %(message)s",
                    datefmt="%I:%M:%S %p",
                    filename='client.log',
                    filemode="w"
                    )

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s  %(name)-7s %(levelname)-8s %(message)s", datefmt="%I:%M:%S %p")
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger('Client')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()

HOST = "localhost"
PORT = 65053

logger.debug('creating socket')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logger.debug('connecting to server')
s.connect((HOST, PORT))

class Message(Thread):
    def __init__(self):
        Thread.__init__(self)
        logger.debug("starting messenger")
        
    def run(self):
        while True:
            try:
                data = s.recv(1024).decode()
            except:
                print("You've been disconnected from the server.")
                return
            if data != "":
                logger.debug('Received: "%s"', data)
                print(data)
                print()
    
# Send a connect message
s.send(bytes("CONNECT", "utf-8"))

messenger = Message()
messenger.start()

while True:
    message = input()
    while message == "":
        print("Well.. say something!")
        message = input()
        
    clear()
    if message.lower() == "/quit":
        logger.debug("Sending DISCONNECT message")
        s.send(bytes("DISCONNECT", "utf-8"))
        s.close()
        break
    else:
        logger.debug('Sending: "%s"', message)
        s.send(bytes(message, "utf-8"))
    
print()
print("Thanks for playing!")