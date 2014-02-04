from Entity import Entity
from Dictionary import WORDS_DICT

class Player(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)
        self._health = 100
        self._defense = 100        
   
    def interpret(self, string):
        string = string.split()
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
            if contains("left", keywords):
                return self.move("LEFT")
            if contains("right", keywords):
                return self.move("RIGHT")
            if contains("backward", keywords):
                return self.move("BACKWARD")
            if contains("forward", keywords):
                return self.move("FORWARD")
            return ("Where do you want to move?")
        
        return ("I don't understand what you mean.")
    
    def move(self, direction):
        """
        Moves character up, down, left, right, forward, and backward.
        """
        directionDict = {"LEFT": (0,-1),
                         "RIGHT": (0,1),
                         "FORWARD": (1,1),
                         "BACKWARD": (1,-1),
                         "UP": (2,1),
                         "DOWN": (2,-1)}
        axis = directionDict[direction][0]
        adjustment = directionDict[direction][1]
        if self.set_position(axis, adjustment):
            return ("Moved to: (" + str(self.get_position(0)) + "," + str(self.get_position(1)) + "," + str(self.get_position(2)) + ")")
        else:
            return ("You can't go that way.")    