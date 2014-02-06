from Entity import Entity
from Dictionary import WORDS_DICT
from Position import Position, Unit

class Player(Entity):
    instances = []
    def __init__(self, name, position = Position([0,0,0])):
        super().__init__(name, position)
        self._health = 100
        self._defense = 100    
        Player.instances.append(self)
   
    def interpret(self, string):
        string = "".join([char for char in string if char.isalnum() or char.isspace()]).lower().split()
        keywords = []
        for word in string:
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
        
        return ("I don't understand what you mean.")
    
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
            return ("Moved to: " + str(self.get_position()))
        else:
            return ("You can't go that way.")    