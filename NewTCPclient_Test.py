import socket, logging, os
from BinaryEncodings import BE
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
                data = s.recv(1024)
                dataType, data = BE.unpack(data)
                dataType = dataType.decode()
                data = data.decode()
                logger.debug('Received a %s type message.', dataType)
            except:
                print("You've been disconnected from the server.")
                return
            if dataType == "MSG":
                logger.debug('Received: "%s"', data)
                print(data)
                print()
            elif dataType == "MAP":
                """
                Right now, this only receives the player's current position and
                nothing else. I'll start to integrate the mob's position, but that
                will take a bit and this is easier.
                
                data will contain a list in the form [0,0,0] of the player's position.
                """
                if data == "INIT":
                    # DUMMY_mapModule.start_map_function()
                    pass #REMOVE THIS LINE
                logger.debug('Received: "%s"', data)

                # I'm going to change this where it will either send all the data and
                # let you parse it, or I'll parse it first, then send it.
                # Or build a parsing module... Maybe that's a bit too much.
                data = data.split(",")
                # DUMMY_mapModule(data)
    
# Send a connect message
s.send(BE.CONNECT)

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
        s.send(BE.DISCONNECT)
        s.close()
        break
    else:
        logger.debug('Sending: "%s"', message)
        s.send(BE.MESSAGE + bytes(message, "utf-8"))
    
print()
print("Thanks for playing!")