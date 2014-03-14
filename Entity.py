import logging

logger = logging.getLogger("Entity")

class Entity:
    def __init__(self, name, visibility, position, parentZone):
        self._name = name
        self._position = position
        self._parentZone = parentZone
        self._visibility = visibility  # Distance radius of visibility.
        self.update_zone()
        
    def __str__(self):
        return self._name
        
    def get_position(self):
        return self._position
    
    def set_position(self, vector, mobbounds=None):
        logger.debug("%s trying to move with vector %s.", self, vector)
        if self._position + vector in self._parentZone:
            if mobbounds is None:
                logger.debug("%s has no mobbounds and is inside %s.", self, self._parentZone)
                self._position += vector
                self.update_zone()
            elif self._position + vector in mobbounds:
                logger.debug("%s is inside mobbounds %s.", self, mobbounds)
                self._position += vector
                self.update_zone()
            return True
        return False

    def can_see(self, other):
        """
        This function returns True or False depending on whether this Entity can visibly see another Entity.
        Currently, things will be able to see through walls. I'll fix that later.
        The check method takes the difference of the two vectors and returns a magnitude which can be checked against.
        """
        logger.debug("%s looking for %s.", self, other)
        distanceVector = self.get_position() - other.get_position()
        distance = sum([abs(axis) for axis in distanceVector])
        return distance <= self._visibility
    
    def update_zone(self):
        """
        Recursive function that keeps track of what Zones and subzones an entity
        is in.
        
        The "zone" begins at the player's parent zone and changes to reflect the
        next layer of zone
        """
        def recursive_subzoning(zone=self._parentZone, tree=[self._parentZone]):
            for subzone in zone.get_subzones():
                if self.get_position() in subzone:
                    tree.append(subzone)
                    return recursive_subzoning(tree[-1], tree)
            return tree
        
        self._ZoneTree = recursive_subzoning()
        return self._ZoneTree
    
    def get_ZoneTree_string(self):
        return " - ".join([str(zone) for zone in self._ZoneTree])

    def set_visibility(self, visibility):
        self._visibility = visibility

    def destruct(self):
        """
        Remove instances of this entity from all lists.
        """
        pass
        
if __name__ == '__main__':
    from Zone import World
    from Position import Position

    e1 = Entity("Entity 1", visibility=3, position=Position([0,0,0]), parentZone=World)