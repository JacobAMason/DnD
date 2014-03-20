# ClientGuiIntercomm.py
"""
This module is responsible for passing data between the client terminal and the Gui.
It will parse MAP data, too, so the client doesn't have to do that.
Both modules import this one and can call its methods to access data.
"""

import logging, GameMap


logger = logging.getLogger("CGI")

GUI = GameMap.PlayerMap()

def send_to_gui(data):
    """
    MAP type packets are parsed here before being sent off to the gui.
    Subtypes:
     S: this player's position (Self)
     P: other players' positions
     M: the position of other Mobs

    Currently, there is no way to distinguish one player from another or
    one mob from another. Only between players, mobs, and the client.

    Whenever the player moves, all the mapping data needed to draw the screen
    will be sent immediately afterwards, so it should be okay to clear the screen
    when the Self is updated.

    data will contain a list in the form [0,0,0] of the player's position.
    """

    if data == "INIT":
        logger.debug('Received MAP INIT')
        GUI.start()

    elif data[0] == "S":
        """
        I'm going to change this where it will either send all the data and
        let you parse it, or I'll parse it first, then send it.
        Or build a parsing module... Maybe that's a bit too much.

        This is the representation of this client's player.
        """
        data = [int(axis) for axis in data[1:].split(",")]
        GUI.client_update(data)
        logger.debug('Received self position: "%s"', data)
        print("You are now at", data)

    elif data == "BEGIN":
        """
        The stream of mob and other player data is about to begin.
        """
        GUI.character_init()
        logger.debug("Starting Map Stream")

    elif data[0] == "P":
        """
        This is the representation of another player.
        """
        data = [int(axis) for axis in data[1:].split(",")]
        GUI.players_update(data)
        logger.debug('Received other player position: "%s"', data)
        print("You see a player at", data)

    elif data[0] == "M":
        """
        This is the representation of a Mob.
        """
        data = [int(axis) for axis in data[1:].split(",")]
        GUI.mob_update(data)
        logger.debug('Received mob position: "%s"', data)
        print("You see a mob at", data)
        
    elif data == "END":
        """
        The stream of mob and other player data is complete.
        """
        GUI.map_update()
        logger.debug("Map Stream Over")
        # don't really need to call anything here