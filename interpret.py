from Dictionary import WORDS_DICT

def contains(container, keywords):
    return any([word in WORDS_DICT[container] for word in keywords])

def interpret(string):
    string = string.split()
    keywords = []
    for word in string:
        keywords.extend([k for k,v in WORDS_DICT.items() if word in v])
        
    if contains("move", keywords):
        if contains("up", keywords):
            return User.move("UP")
        if contains("down", keywords):
            return User.move("DOWN")
        if contains("left", keywords):
            return User.move("LEFT")
        if contains("right", keywords):
            return User.move("RIGHT")
        if contains("backward", keywords):
            return User.move("BACKWARD")
        if contains("forward", keywords):
            return User.move("FORWARD")
        return ("Where do you want to move?")
    
    return ("I don't understand what you mean.")