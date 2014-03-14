from Position import Position

class Zone:
    def __init__(self, name, start, end, parentZone=None, description=None):
        self._bounds = [range(start[0],end[0]),range(start[1],end[1]),range(start[2],end[2])]
        self._lower = start
        self._upper = end
        self._name = name
        self._subzones = []
        self._parentZone = parentZone
        self._description = description
        if parentZone is not None:
            self.create_subzone(parentZone)
            
    def __contains__(self, other):
        """
        The input of other will be a Position object or another zone.
        """
        if isinstance(other, Zone):
            for axis in range(3):
                if other._upper[axis]-1 not in self._bounds[axis]:
                    # -1 on this boundary because upper range is not inclusive
                    print(other._upper[axis], self._bounds[axis])
                    return False
                if other._lower[axis] not in self._bounds[axis]:
                    other._lower[axis], self._bounds[axis]                    
                    return False
        else:
            for axis in range(3):
                if other[axis] not in self._bounds[axis]:
                    return False
        return True
        
    def get_description(self):
        return self._description
    
    def get_subzones(self):
        return self._subzones
        
    def __str__(self):
        return self._name
    
    def create_subzone(self, parentZone):
        if self in parentZone:
            # TODO: check for sister Zones and disallow any overlaps.
            parentZone._subzones.append(self)
            return
        raise Exception("Tried to build zone '" + str(self) + "' outside parent zone '" + str(parentZone) + "'.")


# All the Zones are generated below. The global scope zone "World" is generated
# first, and then all it's subzones are instantiated.

World = Zone("World", Position([0,0,0]), Position([14,14,1]))

def initialize_zones():
    """
    This is a container for the zones since the temporary variables need to expire
    once zoning is completed. The subzones will remain in existence as long as
    World remains in scope.
    """
    z1 = Zone("Test Zone 1", start=Position([0,0,0]), end=Position([5,5,1]), parentZone=World)
    
initialize_zones()