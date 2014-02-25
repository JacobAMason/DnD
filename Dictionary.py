WORDS_DICT = {}

def interpret(self, string, mode):
    """
    Takes any input a given player has typed and acts out the action the input
    has requested.
    The mode is a toggle for special events such as combat or dialogue.
    """
    wordlist = "".join([char for char in string if char.isalnum() or char.isspace()]).lower().split()
    fixedString = " ".join(wordlist)
    keywords = []
    for word in wordlist:
        keywords.extend([k for k,v in WORDS_DICT.items() if word in v])
        
    def contains(container, keywords):
        return any([word in WORDS_DICT[container] for word in keywords])
    
    if mode == "DEFAULT":
        if contains("move", keywords):
            if contains("up", keywords):
                return self.move("UP")
            if contains("down", keywords):
                return self.move("DOWN")
            if contains("west", keywords):
                return self.move("WEST")
            if contains("east", keywords):
                return self.move("EAST")
            if contains("south", keywords):
                return self.move("SOUTH")
            if contains("north", keywords):
                return self.move("NORTH")
            return ("Where do you want to move?")
        
    if mode == "DIALOGUE":
        pass
    
    if fixedString == "where am i":
        return ("You are at coordinate position " + str(self.get_position()) +
                "\nYou have a zone tree of " + str(self.update_zone()))
    
    if fixedString == "save":
        if self.save():
            return ("Saved successfully.")
        else:
            return ("Couldn't save.")
        
    if fixedString == "ping":
        return ("Pong.")
    
    return ("I don't understand what you mean by '" + string + "'.")


WORDS_DICT["move"] = ["go",
                      "move",
                      "climb",
                      "jump",
                      "hike",
                      "venture",
                      "walk",
                      "run",
                      "jog",
                      "fly",
                      "stroll",
                      "meander",
                      "tiptoe"
                      "skip",
                      "step",
                      "leap",
                      "roll",
                      "snake",
                      "creep",
                      "crawl",
                      "wriggle",
                      "grow",
                      "dash",
                      "drive",
                      "zigzag",
                      "slide",
                      "waltz",
                      "hop",
                      "climb",
                      "gallop",
                      "tumble",
                      "skate",
                      "march",
                      "shimmy",
                      "stomp",
                      "polka",
                      "shuffle",
                      "waddle",
                      "moonwalk",
                      "scamper",
                      "prance",
                      "slither",
                      "scoot",
                      "trot"]

WORDS_DICT["up"] = ["up", "above", "ascend"]
WORDS_DICT["down"] = ["down", "below", "descend"]
WORDS_DICT["west"] = ["west"]
WORDS_DICT["east"] = ["east"]
WORDS_DICT["north"] = ["north"]
WORDS_DICT["south"] = ["south"]

WORDS_DICT["yes"] = ["yes",
                     "indeed",
                     "okay",
                     "yep",
                     "alright",
                     "yea",
                     "affirmative",
                     "sure"]

WORDS_DICT["no"] = ["no",
                    "negative",
                    "nope",
                    "nay"]