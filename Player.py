import pickle
from Entity import Entity
from Dictionary import WORDS_DICT
from Position import Position, Unit
from Zone import World

class Player(Entity):
    instances = []
    def __init__(self, name, position=Position([0,0,0]), parentZone=World, password=None):
        super().__init__(name, position, parentZone)
        self._health = 100
        self._defense = 100
        self._password = password
        Player.instances.append(self)
        
    def save(self):
        try:
            users = pickle.load(open("users.p", "rb"))
            users[str(self)] = self
            pickle.dump(users, open("users.p", "wb"))
            return True
        except:
            return False
        
    def check_password(self, password):
        return password == self._password
        
    def interpret(self, string):
        """
        Takes any input a given player has typed and acts out the action the input
        has requested.
        Interprets then executes.
        """
        wordlist = "".join([char for char in string if char.isalnum() or char.isspace()]).lower().split()
        keywords = []
        for word in wordlist:
            keywords.extend([k for k,v in WORDS_DICT.items() if word in v])
            
        def contains(container, keywords):
            return any([word in WORDS_DICT[container] for word in keywords])
            
        if contains("move", keywords):
            if contains("up", keywords):
                return self.move("UP")
            if contains("down", keywords):
                return self.move("DOWN")
            if contains("west", keywords):
                return self.move("WEST")
            if contains("east", keywords):
                return self.move("EAST")
            if contains("south", keywords):
                return self.move("SOUTH")
            if contains("north", keywords):
                return self.move("NORTH")
            return ("Where do you want to move?")
        
        if contains("whereami", keywords):
            return ("You are at coordinate position " + str(self.get_position()))
        
        if string == "save":
            if self.save():
                return ("Saved successfully.")
            else:
                return ("Couldn't save.")
        
        return ("I don't understand what you mean by " + string)
    
    def move(self, direction):
        """
        Moves character up, down, left, right, forward, and backward.
        """
        directionDict = {"WEST": -Unit["i"],
                         "EAST": Unit["i"],
                         "NORTH": Unit["j"],
                         "SOUTH": -Unit["j"],
                         "UP": Unit["k"],
                         "DOWN": -Unit["k"]}
        if self.set_position(directionDict[direction]):
            return ("Moved " + str(self) + " to: " + str(self.get_position()))
        else:
            return ("You can't go that way.")
        
        
        