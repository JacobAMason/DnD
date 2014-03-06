import pickle
from Entity import Entity
import Dictionary
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
        self._interpreterMode = "DEFAULT"
        
    def save(self):
        try:
            users = pickle.load(open("users.p", "rb"))
            users[str(self)] = self
            pickle.dump(users, open("users.p", "wb"))
            return True
        except:
            print("Failed to save.")
            return False

    def manual_append(self):
        """
        When loading, the append to instances is manual.
        """
        Player.instances.append(self)
        
    def check_password(self, password):
        return password == self._password
        
    def interpret(self, string):
        """
        Takes any input a given player has typed and acts out the action the input
        has requested.
        Interprets then executes.
        """
        return Dictionary.interpret(self, string, self._interpreterMode)
    
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

    def destruct(self):
        """
        Performs cleanup by removing the player from all instances lists.
        """
        Player.instances.remove(self)
        super().destruct()
