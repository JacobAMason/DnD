from World import Earth as World

class Entity:
    def __init__(self, name, position):
        self._name = name
        self._health = 0
        self._attackpoints = 0
        self._defense = 0
        self._position = position
        
    def get_position(self, axis):
        return self._position[axis]
    
    def set_position(self, axis, adjustment):
        if self._position[axis] + adjustment in World.bounds(axis):
            self._position[axis] += adjustment
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
        
