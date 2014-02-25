import logging, socketserver, os, pickle, socket, threading, select, time
from BinaryEncodings import BE
from Player import Player
from Connecting import Connecting
from AI import Clock

os.system("title Server")
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# logging system
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)-9s %(levelname)-7s %(message)s",
                    datefmt="%I:%M:%S %p",
                    filename='server.log',
                    filemode="w"
                    )

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(name)-9s %(levelname)-8s %(message)s", datefmt="%H:%M:%S")
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class RequestHandler(socketserver.BaseRequestHandler):
    # "Users" contains all users playing by using a dictionary system where the
    # key is the User's address and the value is their player object.
    USERS = {}
    ADMINS = {}
    
    # "Connecting" is a dictionary of all users who are in the process of
    # connecting to the server where the key is their address and the value is
    # the Connecting object.
    CONNECTING = {}

    # This makes it possible to send all the clients a broadcast
    REQUESTS = []
    
    # This lets one IP address run multiple clients if True
    ALLOW_MULTIPLE_CONNECTIONS = True

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('RHandler')
        self.logger.debug('__init__')
        self.address = client_address
        self.request = request
        RequestHandler.REQUESTS.append(self.request)
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')
        return socketserver.BaseRequestHandler.setup(self)

    def handle(self):
        self.logger.debug('handle')

        # Respond
        while True:
            try:
                data = self.request.recv(1024)
            except:
                return

            # unpack the message
            dataType, data = BE.unpack(data)
            dataType = dataType.decode()
            data = data.decode()
            
            self.logger.debug('Server received a %s type message.', dataType)
            self.logger.debug('Server received: "%s"', data)
            # RESPONSE will contain the string to be sent to the address.
            RESPONSE = ""
            
            if dataType == "DIS":
                return
            
            elif self.address in RequestHandler.USERS:
                RESPONSE = RequestHandler.USERS[self.address].interpret(data)
                
                self.logger.debug("Sender: %s at %s", RequestHandler.USERS[self.address], self.address)
                self.logger.debug("Received: %s", data)
                self.logger.debug("Replying with: %s", RESPONSE)
                        
            elif self.address in RequestHandler.CONNECTING:
                if RequestHandler.CONNECTING[self.address].get_status() == "UNKNOWN":
                    if data.lower() == "load":
                        RequestHandler.CONNECTING[self.address].set_status("LOAD")
                        RESPONSE = ("Okay.\nWhat is your username?")
                    elif data.lower() == "new":
                        RequestHandler.CONNECTING[self.address].set_status("NEW")
                        RESPONSE = ("Okay.\nWhat would you like your username to be?")
                    else:
                        RESPONSE = ("I didn't catch that.\nType 'load' or 'new' to proceed.")
                        
                elif RequestHandler.CONNECTING[self.address].get_status() == "LOAD":
                    RESPONSE = RequestHandler.CONNECTING[self.address].load(data)
                    
                elif RequestHandler.CONNECTING[self.address].get_status() == "NEW":
                    RESPONSE = RequestHandler.CONNECTING[self.address].new(data)
                
                if RequestHandler.CONNECTING[self.address].get_status() == "CONNECTED":
                    RequestHandler.USERS[self.address] = RequestHandler.CONNECTING[self.address].generate()
                    self.logger.info('[+] User "%s" has joined at %s', str(RequestHandler.USERS[self.address]), self.address)
                    del RequestHandler.CONNECTING[self.address]
                    
            elif dataType == "CON":
                if ((any([key[0] == self.address[0] for key in RequestHandler.USERS.keys()]) or
                  any([key[0] == self.address[0] for key in RequestHandler.CONNECTING.keys()])) and
                  not RequestHandler.ALLOW_MULTIPLE_CONNECTIONS):
                    self.logger.warn("[!] Client at %s is attempting to connect multiple times.", self.address)
                    RESPONSE = ("You are already connected.")
                    return
                else:
                    self.logger.info("[+] New client connecting at: %s", self.address)
                    RequestHandler.CONNECTING[self.address] = Connecting()
                    RESPONSE = ("Welcome to the server!\nType 'load' or 'new' to proceed.")

            
            # Admin cases below which probably won't be used much longer.
            elif data == "ADMIN LOGIN 42":
                self.logger.info("[^] Admin connecting at: %s", self.address)
                
                RequestHandler.ADMINS[self.address] = Player("Admin " + str(len(RequestHandler.ADMINS)+1))
                
                RESPONSE = ("Welcome, admin!")
                
            elif self.address in RequestHandler.ADMINS:
                if data == "SHUTDOWN":
                    RESPONSE = ("Shutting down server!")
                    self.logger.warn("[^] Shutting down!")
                    SHUTDOWN_RESTART = "SHUTDOWN"
                elif data == "RESTART":
                    RESPONSE = ("Restarting server!")
                    self.logger.warn("[^] Restarting!")
                    SHUTDOWN_RESTART = "RESTART"  
                self.logger.info("[^] Executing adminitrator command: %s", data)
                try:
                    exec(data)
                    RESPONSE = ("It has been done.")
                    self.logger.info("[^] SUCCESS")
                except Exception as errorMSG:
                    RESPONSE =("Erm... That didn't go as planned:\n"+str(errorMSG))
                    self.logger.warn("[^] FAILURE")
                    
            else:
                self.logger.warn("[!] Something fishy coming from %s.", self.address)
                self.logger.warn('    They sent "%s"', data)
                RESPONSE = ("Modded Client? Want the ban hammer?")
            
            # RESPOND
            self.request.send(BE.MESSAGE + bytes(RESPONSE, "utf-8"))

    def finish(self):
        if self.address in RequestHandler.USERS:
            self.logger.info("[-] User %s:%s disconnected.", RequestHandler.USERS[self.address], self.address)
            del RequestHandler.USERS[self.address]
        elif self.address in RequestHandler.ADMINS:
            self.logger.info("[-] Admin %s:%s disconnected.", RequestHandler.ADMINS[self.address], self.address)
            del RequestHandler.ADMINS[self.address]
        elif self.address in RequestHandler.CONNECTING:
            self.logger.info("[-] Client %s disconnected.", self.address)
            del RequestHandler.CONNECTING[self.address]
        RequestHandler.REQUESTS.remove(self.request)
        return socketserver.BaseRequestHandler.finish(self)


class Server(socketserver.ThreadingTCPServer):
    
    def __init__(self, server_address, handler_class=RequestHandler):
        self.logger = logging.getLogger('Server')
        self.logger.debug('__init__')
        socketserver.ThreadingTCPServer.allow_reuse_address = False
        socketserver.ThreadingTCPServer.__init__(self, server_address, handler_class)
        self.__is_shut_down = threading.Event()
        self.__shutdown_request = False
        return

    def server_activate(self):
        self.ip, self.port = self.server_address
        self.logger.info('Started server on %s:%s', self.ip, self.port)
        socketserver.ThreadingTCPServer.server_activate(self)
        # Start game clock
        self.GAMECLOCK = Clock()
        self.GAMECLOCK.start()
        return

    def serve_forever(self, poll_interval=0.5):
        """Handle one request at a time until shutdown.

        Polls for shutdown every poll_interval seconds. Ignores
        self.timeout. If you need to do periodic tasks, do them in
        another thread.
        """
        self.logger.info('Online and waiting for requests.')
        self.__is_shut_down.clear()
        try:
            while not self.__shutdown_request:
                r, w, e = select.select([self], [], [], poll_interval)
                if self in r:
                   self.handle_request()
        finally:
            self.__shutdown_request = False
            self.__is_shut_down.set()

    # def serve_forever(self):
    #     self.logger.info('Online and waiting for requests.')
    #     while True:
    #         self.handle_request()
    #     return

    def handle_request(self):
        self.logger.debug('Waiting for requests.')
        return socketserver.ThreadingTCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        self.logger.debug('verify_request(%s, %s)', request, client_address)
        return socketserver.ThreadingTCPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        self.logger.debug('process_request(%s, %s)', request, client_address)
        return socketserver.ThreadingTCPServer.process_request(self, request, client_address)

    def finish_request(self, request, client_address):
        self.logger.debug('finish_request(%s, %s)', request, client_address)
        return socketserver.ThreadingTCPServer.finish_request(self, request, client_address)

    def close_request(self, request):
        self.logger.debug('close_request(%s)', request)
        return socketserver.ThreadingTCPServer.close_request(self, request)

    def shutdown(self, t):
        """Stops the serve_forever loop.

         Blocks until the loop has finished. This must be called while
         serve_forever() is running in another thread, or it will
         deadlock.
        """
        if t != 0:
            self.logger.warn('[!] Server shutdown in %s seconds!', t)
            time.sleep(t)
        self.__shutdown_request = True
        self.__is_shut_down.wait()
        self.logger.warn('[!] Server going down!')
        self.GAMECLOCK.stop()


def start_server():
    address = ('localhost', 65053) # let the kernel give us a port
    server = Server(address, RequestHandler)
    ip, port = server.server_address # find out what port we were given

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True) # don't hang on exit
    t.start()
    return server, t


def broadcast(message):
    """
    Sends a message to all connected clients.
    """
    for request in RequestHandler.REQUESTS:
        request.send(BE.MESSAGE + bytes(message, "utf-8"))


# Build the interface so commands can be run from the server window.
class Injection(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def launch(self):
        self.serverObj, self.serverThread = start_server()
        
    def shutdown(self, t=0):
        self.serverObj.shutdown(t)

    def restart(self):
        self.shutdown()
        self.launch()
    
    def run(self):
        print("Injector online.")
        while True:
            try:
                command = input()
                if command.lower() =="":
                    continue
                elif command.lower() in ["launch","start"]:
                    self.launch()
                elif command.lower() == "restart":
                    self.restart()
                elif command.lower().split()[0] in ["shutdown","quit","stop"]:
                    try:
                        self.shutdown(int(command.lower().split()[1]))
                    except IndexError:
                        self.shutdown()
                else:
                    exec(command)
            except KeyboardInterrupt:
                exit(0)
            # except Exception as errorMSG:
            #     print(errorMSG)

Injector = Injection()
Injector.setDaemon(False)
Injector.start()