# MapGenerator.py
"""
MapGenerator keeps all the coordinate positions of all entities in the same location.
It offers methods for determining the location of other entities in any given player's radius.
MapGenerator is mostly used to determine a Player's visible range, but it can also be used
by mobs to determine what is in proximity to them.

MapGen will send MAP type packets with an additional prefix to distinguish between
self movement confirmation and the locations of other players and entities.
"""
import logging
from BinaryEncodings import BE
from Mob import Mob

# Future use for when the map should display other people and things.
# from Player import Player
# from Mob import Mob

logger = logging.getLogger("Mapper")

class MapGenerator:
    def __init__(self):
        logger.info("MapGen: Online")

    def start(self, player, pInstances):
        """
        Sends the "start" command to the client so the gui will initialize.
        """
        logger.debug("Sending MAP INIT.")
        player.request.send(BE.MAP + bytes("INIT", "utf-8"))
        self.update_position(player, pInstances)

    def update_position(self, player, pInstances):
        """
        Sends a packet to an player that contains his current position.
        Players usually call this upon updating their positions.
        """
        logger.debug("Sending %s MAP data.", player)
        player.request.send(BE.MAP + bytes("S" + str(player.get_position())[1:-1], "utf-8"))  # 1 to -1 removes the "[" characters
        self.refresh_view(pInstances)

    def refresh_view(self, pInstances):
        """
        Returns map data based on an player's visible radius.
        When any Player moves or after every 10 seconds, this function will loop over all the Player entities.
        It will check to see which player/mobs see who and then send map data to the corresponding players.
        """
        logger.debug("Refreshing view.")
        for p in pInstances:
            p.request.send(BE.MAP + bytes("BEGIN", "utf-8"))
            for other in pInstances:
                if p is not other and p.can_see(other):
                    logger.debug("Sending %s the position of %s", p, other)
                    p.request.send(BE.MAP + bytes("P" + str(other.get_position())[1:-1], "utf-8"))
            for other in Mob.instances:
                if p.can_see(other):
                    logger.debug("Sending %s the position of %s", p, other)
                    p.request.send(BE.MAP + bytes("M" + str(other.get_position())[1:-1], "utf-8"))
                if other.can_see(p):
                    logger.debug("%s has spotted %s", other, p)
                    p.request.send(BE.MESSAGE + bytes("You've been spotted by a " + str(other) + ".", "utf-8"))
            p.request.send(BE.MAP + bytes("END", "utf-8"))



MapGen = MapGenerator()