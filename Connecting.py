import pickle
from Player import Player

class Connecting:
    """
    Generates a new player. Every if section checks for the current creation
    step.
    """        
    def __init__(self):
        self._status = "UNKNOWN"
        self._step = 0   
    
    def get_status(self):
        return self._status
    
    def set_status(self, status):
        self._status = status
        
    def new(self, message):
        if self._step == 0:
            try:
                self._users = pickle.load(open("users.p", "rb"))
            except:
                self._users = {}

            if not message.isalnum():
                return ("Try only using alpha-numeric characters.")
            elif message not in self._users:
                self._step = 1
                self._name = message
                return ("Okay, " + self._name + ". Is that what you wish to be called?")
            else:
                return ("Sorry, that name has already been taken.\nTry another.")
            
        elif self._step == 1:
            if message.lower()[0] == "y":
                self._step = 2
                return ("Okay, " + self._name +
                        ".\nWhat would you like your password to be?" +
                        "\nWARNING: It will be visible when you type it.")
            else:
                self._step = 0
                return ("Okay. What would you like to be called?")
            
        elif self._step == 2:
            self._password = message
            self._step = 3
            return ("Please type it again, just to be sure.") 
        
        elif self._step == 3:
            if self._password == message:
                self.set_status("CONNECTED")
                self._player = Player(self._name, password=self._password)
                
                try:
                    self._users = pickle.load(open("users.p", "rb"))
                except:
                    self._users = {} 
                    
                self._users[str(self._player)] = self._player
                
                pickle.dump(self._users, open("users.p", "wb"))
                
                return ("Got it.\n\nWelcome to the server, " + self._name +"!")
            else:
                self._step = 2
                return ("Oops. Those didn't match.\nLet's try that again." +
                        "\nWhat would you like your password to be?" +
                        "\nWARNING: It will be visible when you type it.")                        
            
    def load(self, message):
        try:
            self._users = pickle.load(open("users.p", "rb"))
        except:
            self._users = {}  
            
        if self._step == 0:
            if message in self._users:
                self._name = message
                self._step = 1
                return ("Enter your password" +
                        "\nWARNING: It will be visible when you type it.")
            else:
                self.set_status("UNKNOWN")
                self._step = 0
                return ("Sorry. I can't seem to find that username." +
                        "\n\nType 'load' or 'new' to proceed.")
            
        elif self._step == 1:
            if self._users[self._name].check_password(message):
                self.set_status("CONNECTED")
                self._player = self._users[self._name]
                return ("Welcome back, " + str(self._player) + "!")
            else:
                self.set_status("UNKNOWN")
                self._step = 0
                return ("Sorry. That password is incorrect." +
                        "\n\nType 'load' or 'new' to proceed.")    
            
    def generate(self):
        return self._player
            
