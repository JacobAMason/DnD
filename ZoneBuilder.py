# ZoneBuilder.py
"""
Module used for generating new zones.
"""
import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def build(xaxis, yaxis, zaxis):
    """
    Generates the base room numbers
    """
    matrix = []
    for floor in range(zaxis):
        roomnum = 1
        matrix.append([])
        for row in range(yaxis):
            matrix[floor].append([])
            for column in range(xaxis):
                matrix[floor][row].append(str(roomnum))
                roomnum += 1
    return matrix


def display(zone, floor, walls=False):
    """
    Prints an interpretation of a single floor of a 3d area.

    Optional parameter "walls" will indicate that the cells contain wall data that needs to be
    interpreted. Otherwise, the cell data is considered to be a generic room number.
    """
    print("Floor", floor+1)
    matrix = zone[floor]
    # Print the matrix.
    anMaxSizes = [0 for column in range(len(matrix[0]))]
    
    # The below loop fills the Max Sizes list with the space each column
    # will need.
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            nSizeOfChar = len(str(matrix[row][column]))
            if nSizeOfChar > anMaxSizes[column]:
                anMaxSizes[column] = nSizeOfChar
                
    # Create and print lines.
    sBuffer = ""
    if walls:
        sBuffer += "_"*(sum(anMaxSizes)) + "_"*2*(len(anMaxSizes)) + "\n"

        # This sections builds the north walls on the top row
        for column in range(len(matrix[row])):
            if walls:
                cellBin = bin(matrix[row][column])[2:].zfill(6)
            else:
                cellBin = "000000"

            sBuffer += " "
      
            if cellBin[2] == "1":
                sStringToCat = format("-", ">" + str(anMaxSizes[column]))
            else:
                sStringToCat = format(" ", ">" + str(anMaxSizes[column]))

            sBuffer += sStringToCat
            sBuffer += " "
        sBuffer += "\n"
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            if walls:
                cellBin = bin(matrix[row][column])[2:].zfill(6)
            else:
                cellBin = "000000"

            if walls and cellBin[3] == "1":
                sBuffer += "|"
            else:
                sBuffer += " "

            if matrix[row][column] == -1:
                sStringToCat = format(" ", ">" + str(anMaxSizes[column]))
            else:
                sStringToCat = format(matrix[row][column], ">" + str(anMaxSizes[column]))
            
            sBuffer += sStringToCat
            
            if walls and cellBin[1] == "1":
                sBuffer += "|"
            else:
                sBuffer += " "
        sBuffer += "\n"

        if not walls:
            continue

        # This sections builds the north and south walls and shouldn't execute when walls isn't True
        for column in range(len(matrix[row])):
            if walls:
                cellBin = bin(matrix[row][column])[2:].zfill(6)
            else:
                cellBin = "000000"
      
            if cellBin[2] == "1":
                sStringToCat = format("----", ">" + str(anMaxSizes[column]))
            else:
                sStringToCat = format("    ", ">" + str(anMaxSizes[column]))

            sBuffer += sStringToCat
        sBuffer += "\n"
    print(sBuffer)
    return


def dimensions():
    clear()
    print("Welcome to the zone builder.")
    print("I'm going to walk you through building a zone.")
    print()
    print("First, I'm going to need to know the dimensions of your zone.")
    print("How many floors should the zone have?")
    print()
    loop = True
    while loop:
        try:
            zaxis = int(input(">> "))
        except:
            clear()
            print("Let's try that again.")
            print("How many floors should the zone have?")
        else:
            loop = False
    clear()
    print("Okay,", zaxis, "floors it is.")
    print()
    print("How long should the x-axis of the zone be?")
    print()
    loop = True
    while loop:
        try:
            xaxis = int(input(">> "))
        except:
            clear()
            print("Let's try that again.")
            print("How long should the x-axis of the zone be?")
        else:
            loop = False
    clear()
    print("Okay,", xaxis, "squares.")
    print()
    print("How long should the y-axis of the zone be?")
    print()
    loop = True
    while loop:
        try:
            yaxis = int(input(">> "))
        except:
            clear()
            print("Let's try that again.")
            print("How long should the x-axis of the zone be?")
        else:
            loop = False
    clear()
    print("Okay,", yaxis, "squares.")
    print()
    print("Lets start building the rooms.")
    print("I'm going to prompt you with a room coordinate and I'd like you to respond to my questions.")
    print("At the end, you'll have the opportunity to fix any mistakes you made in the process.")
    print("Press the enter key to proceed.")
    input()
    return build(xaxis, yaxis, zaxis), xaxis, yaxis, zaxis


def swap_states(matrix, floor, xaxis, rooms):
    """
    This algorithm subracts the selection by the number of rooms per row
    so that the column can be determined. The number of subtraction loops
    also tells us the row the room is in.
    """
    for room in rooms:
        try:
            column = room
            row = 1
            while column > xaxis:
                column -= xaxis
                row += 1

            row -=1
            column -=1

            if column == -1:
                # catches a case when the user enters 0 as a room number.
                # would originally toggle the last element on the first row.
                continue

            if "Y" in matrix[floor][row][column]:
                matrix[floor][row][column] = matrix[floor][row][column].replace("Y", "")
            else:
                matrix[floor][row][column] = "Y" + matrix[floor][row][column]
            # Row and column now contain the coordinates of the room.
        except IndexError:
            print()
            print(room,"isn't one of the room numbers.")
            print("Press enter keep working.")
            input()
    return matrix


def remove_Ys(matrix, xaxis, yaxis, zaxis):
    for floor in range(zaxis):
        for row in range(yaxis):
            for column in range(xaxis):
                    if "Y" in matrix[floor][row][column]:
                        matrix[floor][row][column] = matrix[floor][row][column].replace("Y", "")
                    else:
                        matrix[floor][row][column] = -1
        display(matrix,floor)
    return matrix


def existance(matrix, xaxis, yaxis, zaxis):
    for floor in range(zaxis):
        while True:
            clear()
            print("Okay. I'm going to show a floor plan of your zone with numbers inside the")
            print("individual rooms. I'd like you to tell me the room numbers which will be")
            print("used in this zone. You may enter them in the form or a space or comma")
            print("delimited list or one at a time. \nWhen you are done, enter 'q'\n\n")
            display(matrix, floor)

            sInput = input(">> ")
            if sInput.lower() == "q":
                break

            matrix = swap_states(matrix, floor, xaxis, set(map(int, sInput.replace(","," ").split())))

    clear()
    return remove_Ys(matrix, xaxis, yaxis, zaxis)


def enclose_rooms(matrix, xaxis, yaxis, zaxis):
    """
    This function preps the matrix for wall generation. 
    First, it removes the leftover room numbers.
    Second, it generates walls where a room is adjacent to a void space.
    """
    newMatrix = [[[-1 for x in range(xaxis)] for y in range(yaxis)] for z in range(zaxis)]
    for floor in range(zaxis):
        for row in range(yaxis):
            for column in range(xaxis):
                if matrix[floor][row][column] != -1:
                    bitstring = 0b000011
                    # North
                    if row == 0 or matrix[floor][row-1][column] == -1:
                        bitstring += 0b100000
                    # East
                    if column+1 == xaxis or matrix[floor][row][column+1] == -1:
                        bitstring += 0b010000
                    # South
                    if row+1 == yaxis or matrix[floor][row+1][column] == -1:
                        bitstring += 0b001000
                    # West
                    if column == 0 or matrix[floor][row][column-1] == -1:
                        bitstring += 0b000100
                    newMatrix[floor][row][column] = bitstring
    return newMatrix


def select_walls(matrix, xaxis, yaxis, zaxis):
    """
    This section is responsible for creating walls within each room.
    """
    clear()
    print("Now we're going to construct the interior of the rooms.")
    print("I'm going to present you with all rooms that have been selected.")
    print("I want you to indicate where the walls should be placed in each room.")
    print("Just like room selection, you will indicate, by a list of numbers,")
    print("where the walls should be placed.")
    print()
    print("In locations where a room is adjacent to a void space, a non-optional")
    print("will automatically be inserted. Later some of these can be removed")
    print("to create vertical trasversals, but for now, just consider each")
    print("floor individually.")


def ZoneBuilder():
    """
    This is a modification of the matrix builder. Now used to input manual zone data.
    """

    # Part 1: Zone Dimensions
    matrix, xaxis, yaxis, zaxis = dimensions()

    # Part 2: Assigning Room Existance.
    matrix = existance(matrix, xaxis, yaxis, zaxis)
    
    # Part 3: Creating room walls.
    
    # First, generate walls adjacent to void spaces.
    matrix = enclose_rooms(matrix, xaxis, yaxis, zaxis)
    
    matrix = select_walls(matrix, xaxis, yaxis, zaxis)


if __name__ == '__main__':
    m1 = build(5, 5, 2)
    m1 = swap_states(m1, floor=0, xaxis=5, rooms=[1,2,3,4,5,14,16,17,13,18])
    m1 = swap_states(m1, floor=1, xaxis=5, rooms=[20,21,23,24,25,17,19,13,14,4,8])
    m1 = remove_Ys(m1, 5, 5, 2)
    m1 = enclose_rooms(m1, 5, 5, 2)
    display(m1, 0, 1)
    display(m1, 1, 1)