import socket, logging, os, GameMap
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

HOST = "25.122.108.67"
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
                raw = s.recv(1024)
            except:
                print("You've been disconnected from the server.")
                return

            packetList = BE.parse(raw)

            for dataType, data in packetList:

                logger.debug('Received a %s type message.', dataType)
                logger.debug('Message contains: "%s"', data)

                if dataType == "MSG":
                    print(data)
                    print()
                elif dataType == "MAP":
                    """
                    MAP type packets are parsed here before being sent off to the gui.
                    Subtypes:
                     S: this player's position (Self)
                     P: other players' positions
                     M: the position of other Mobs

                    Currently, there is no way to distinguish one player from another or
                    one mob from another. Only between players, mobs, and the client.

                    Whenever the player moves, all the mapping data needed to draw the screen
                    will be sent immediately afterwards, so it should be okay to clear the screen
                    when the Self is updated.
                    
                    data will contain a list in the form [0,0,0] of the player's position.
                    """

                    if data == "INIT":
                        logger.debug('Received MAP INIT')
                        MyMap = GameMap.PlayerMap([0,14,0])
                        MyMap.start()

                    elif data[0] == "S":
                        """
                        I'm going to change this where it will either send all the data and
                        let you parse it, or I'll parse it first, then send it.
                        Or build a parsing module... Maybe that's a bit too much.

                        This is the representation of this client's player.
                        """
                        data = [int(axis) for axis in data[1:].split(",")]
                        MyMap.client_update(data)
                        logger.debug('Received self position: "%s"', data)
                        print("You are now at", data)

                    elif data == "BEGIN":
                        """
                        The stream of mob and other player data is about to begin.
                        """
                        MyMap.character_init()
                        logger.debug("Starting Map Stream")

                    elif data[0] == "P":
                        """
                        This is the representation of another player.
                        """
                        data = [int(axis) for axis in data[1:].split(",")]
                        MyMap.players_update(data)
                        logger.debug('Received other player position: "%s"', data)
                        print("You see a player at", data)

                    elif data[0] == "M":
                        """
                        This is the representation of a Mob.
                        """
                        data = [int(axis) for axis in data[1:].split(",")]
                        MyMap.mob_update(data)
                        logger.debug('Received mob position: "%s"', data)
                        print("You see a mob at", data)
                        
                    elif data == "END":
                        """
                        The stream of mob and other player data is complete.
                        """
                        logger.debug("Map Stream Over")
                        # don't really need to call anything here

    
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