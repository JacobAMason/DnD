import Dice
from Entity import Entity
from Position import Position, Unit

class Mob(Entity):
    instances = []
    def __init__(self, name, position, wander, speed):
        super().__init__(name, position)
        self._bounds = [range(position[0] - wander, position[0] + wander),
                        range(position[1] - wander, position[1] + wander),
                        range(position[2] - wander, position[2] + wander)]
        self._speed = speed
        Mob.instances.append(self)
        
    def get_speed(self):
        """
        Speed is needed by the AI to know how often to move a Mob.
        """
        return self._speed
        
    def get_bounds(self, axis):
        return self._bounds[axis]
        
    def move(self):
        """
        Mobs move differently than Players. Their position is self-calculated,
        so there is no need for any parameters to be passed to it. It, however,
        will pass a position to Entity's move method. Each Mob has a wander
        radius that it won't move outside.
        A game clock will cycle through all Mobs in existence, moving each of
        them at a random time interval. A Mob's _speed will determine how often
        the game's AI move's all the Mobs.
        """
        movementSuccess = False
        
        directions = {1:Unit["i"], 2:-Unit["i"], 3:Unit["j"], 4:-Unit["j"], 5:Unit["k"], 6:-Unit["k"]}
        
        while not movementSuccess:
            vector = directions[Dice.roll(1,6)]
            
            if self.set_position(vector):
                print("Attempting to move", self._name)
                movementSuccess = True
            else:
                movementSuccess = False
                print("Not in wander radius.")
                
        print("Moved to", self.get_position())
        
        
        
m1 = Mob("Zombie", Position([0,0,0]), 3, 10)