class Entity:
    def __init__(self, name, position, parentZone):
        self._name = name
        #self._health = 0
        #self._attackpoints = 0
        #self._defense = 0
        self._position = position
        self._parentZone = parentZone
        self.update_zone()
        
    def __str__(self):
        return self._name
        
    def get_position(self):
        return self._position
    
    def set_position(self, vector, mobbounds=None):
        if self._position + vector in self._parentZone:
            if mobbounds is None:
                self._position += vector
            elif self._position + vector in mobbounds:
                self._position += vector
            self.update_zone()
            return True
        return False
    
    def update_zone(self):
        """
        Recursive function that keeps track of what Zones and subzones an entity
        is in.
        
        The "zone" begins at the player's parent zone and changes to reflect the
        next layer of zone
        """
        def recursive_subzoning(zone=self._parentZone, tree=[]):
            for subzone in zone.get_subzones():
                if self.get_position() in subzone:
                    tree.append(subzone)
                    return recursive_subzoning(tree[-1], tree)
            return tree
        
        self._ZoneTree = recursive_subzoning()
        return self._ZoneTree
    
    def get_ZoneTree_string(self):
        return " - ".join([str(zone) for zone in self._ZoneTree])
        
        
    #def take_damage(self, damage):
        #damage =- self._armor
        #if damage > 0:
            #self._health - damage
            
    #def add_health(self, health):
        #self._health += health
            
    #def deal_damage(self, other):
        #self._attackpoints
        
