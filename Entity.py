from World import Earth as World
from Position import Position, Unit

class Entity:
    def __init__(self, name, position):
        self._name = name
        self._health = 0
        self._attackpoints = 0
        self._defense = 0
        self._position = position
        
    def get_position(self):
        return self._position
    
    def set_position(self, vector):
        if self._position + vector in World:
            self._position += vector
            return True
        return False
        
    #def take_damage(self, damage):
        #damage =- self._armor
        #if damage > 0:
            #self._health - damage
            
    #def add_health(self, health):
        #self._health += health
            
    #def deal_damage(self, other):
        #self._attackpoints
        
