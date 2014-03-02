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


def display(zone, floor):
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
    for row in range(len(matrix)):
        sBuffer += "|"
        for column in range(len(matrix[row])):
            if matrix[row][column] == -1:
                sStringToCat = format(" ", ">" + str(anMaxSizes[column] + 1))
            else:
                sStringToCat = format(matrix[row][column], ">" + str(anMaxSizes[column] + 1))
            sBuffer += sStringToCat + " "
        sBuffer += "|\n"
    
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

            for room in set(map(int, sInput.replace(","," ").split())):
                """
                This algorithm subracts the selection by the number of rooms per row
                so that the column can be determined. The number of subtraction loops
                also tells us the row the room is in.
                """
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
    clear()
    for floor in range(zaxis):
        for row in range(yaxis):
            for column in range(xaxis):
                    if "Y" in matrix[floor][row][column]:
                        matrix[floor][row][column] = matrix[floor][row][column].replace("Y", "")
                    else:
                        matrix[floor][row][column] = -1
        display(matrix,floor)




def ZoneBuilder():
    """
    This is a modification of the matrix builder. Now used to input manual zone data.
    """

    # Part 1: Zone Dimensions
    matrix, xaxis, yaxis, zaxis = dimensions()

    # Part 2: Assigning Room Existance.
    existance(matrix, xaxis, yaxis, zaxis)    