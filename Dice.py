import random

def roll(quantity, faces):
    """
    Rolls dice. 2d6 would be used like roll(2,6)
    """
    return sum([random.randint(1,faces) for i in range(quantity)])