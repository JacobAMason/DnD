import Dice, logging
from Entity import Entity
from Zone import Zone, World
from Position import Position, Unit

logger = logging.getLogger("Mob")

class Mob(Entity):
    instances = []
    def __init__(self, name, visibility=3, position=Position([0,0,0]), speed=10, wander=None, follows=True, parentZone=World):
        """
        This is the standard Mob class for all Mobs that passively move around
        in the world.
        
        Mobs are restricted to the parent zone they were created in as well as
        their own wander radius. The center of their wander radius will change
        as their position changes. This is because as a Mob "sees" a Player,
        they will approach that player, updating their anchor and, consequently,
        their wander radius.
        
        The wander radius is stored as a Zone object. (Not as a subzone, however,
        because that would prevent the Mob from approaching the world bounderies).
        
        Example Mob:
        
        name = "Zombie"
        position = Position([0,0,0])
        wander = 3
        speed = 10
        """
        super().__init__(name, visibility, position, parentZone)
        self._position = position
        if wander is not None:
            self._zone = Zone(name="Mob Wander Radius",
                              start=Position([self._position[0] - wander,
                                              self._position[1] - wander,
                                              self._position[2] - wander]),
                              end=Position([self._position[0] + wander +1,
                                            self._position[1] + wander +1,
                                            self._position[2] + wander +1]))
        else:
            self._zone = None  # Setting this to None causes set_position() to not check it at all.
        self._speed = speed
        self._willFollow = True  # All mobs will follow by default.
        self._wasFollowing, self._isFollowing = [], []
        Mob.instances.append(self)
        
    def get_speed(self):
        """
        Speed is needed by the AI to know how often to move a Mob.
        """
        return self._speed
        
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
        
        directions = {1:Unit["i"], 2:-Unit["i"], 3:Unit["j"],
                      4:-Unit["j"], 5:Unit["k"], 6:-Unit["k"]}
        
        while not movementSuccess:
            vector = directions[Dice.roll(1,6)]
            
            if self.set_position(vector, mobbounds=self._zone):
                movementSuccess = True
                
        logger.debug("Moved %s to %s.", self, self.get_position())


    # Player tracking functions

    def follow(self, other):
        """
        This function adds the player to a tracking list, choosing only the closest as the
        primary target.
        """
        self._isFollowing.append(other)
        for i in range(1, len(self._isFollowing)):
            while i > 0 and (self._isFollowing[i-1].get_position() - self.get_position()) > (self._isFollowing[i].get_position() - self.get_position()):
                self._isFollowing[i], self._isFollowing[i-1] = self._isFollowing[i-1], self._isFollowing[i]
                i -=1
        logger.debug("%s is tracking %s", self, other)

    def can_see(self, other):
        """
        This function is a bit weird. It is kinda like a mask for the underlying can_see()
        function that resides in the parent class Entity. This function basically passes the
        function call through, but can make changes on this particular subclass level in 
        the process.
        It does this so the Mob can effectively "follow" players around.
        """
        if super().can_see(other):
            if self._willFollow:
                self.follow(other)
            return True
        else:
            if self._willFollow and other in self._wasFollowing:
                self._isFollowing.remove(other)
            return False


    def destruct(self):
        """
        Performs cleanup by removing the mob from all instances lists.
        """
        Mob.instances.remove(self)
        super().destruct()
        self = None

# Temp test Mob
m1 = Mob(name="Zombie", visibility=3, position=Position([0,0,0]), speed=10, wander=None, follows=True, parentZone=World)