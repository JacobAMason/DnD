class Entity:
    def __init__(self, name, position, parentZone):
        self._name = name
        self._health = 0
        self._attackpoints = 0
        self._defense = 0
        self._position = position
        self._parentZone = parentZone
        
    def __str__(self):
        return self._name
        
    def get_position(self):
        return self._position
    
    def set_position(self, vector, mobbounds=None):
        if self._position + vector in self._parentZone:
            if mobbounds is None:
                self._position += vector
                return True
            elif self._position + vector in mobbounds:
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
        
