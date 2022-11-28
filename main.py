# main.py

import re
import expression
from expression import *

def users_choice():
    """
    User says in which way he has entered the data:
    1 - By writing formula of the function in formula.txt
    2 - By writing coordinates of n points in coordinates.txt
    """
    inp = 0
    end = False
    while (not end):
        try:
            inp = int(input("""Enter 1, if you set the function in coordinates.txt
Enter 2, if you set the function in formula.txt\n"""))
        except:
            print('Incorrect input! Please, try again')
        else:
            if inp in [1, 2]:
                end = True
            else:
                print('Incorrect input! Please, try again')

    return inp


def integral_by_coordinates():
    """
    Calculates the integral by n coordinates from coordinates.txt
    """
    def trapezoid_formula(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2

        return (x2-x1) * (y1 + y2)/2


    # Get the data from coordinates.txt file: 
    with open("coordinates.txt", 'r') as f:
        f.seek(0)
        lines = f.readlines()
    
        n = 0
        a = b = 0.0
        line_ind = 0 # index of line, after which are going to be lines with values(only of coords)

        for i, line in enumerate(lines):
            # finds the value of n
            match_n = re.search(r'n\s*=\s*', line)
            if match_n != None:
                value = re.findall(r'[\d]+', line)
                n = int(value[0])

            # finds value of a
            match_a = re.search(r'a\s*=\s*', line)
            if match_a != None:
                value = re.findall(r'[\d.-]+', line)
                a = float(value[0])

            # finds value of b
            match_b = re.search(r'b\s*=\s*', line)
            if match_b != None:
                value = re.findall(r'[\d.-]+', line)
                b = float(value[0])

            # find the index of line, which is "Enter coordinates of n points through the space"
            if "coordinates of n points through the space" in line:
                line_ind = i

        coord_list = []
        for line in lines[line_ind:]:
            matches = re.findall(r'[\d.-]+', line)
            if len(matches) == 2:
                coord_list.append( (float(matches[0]), float(matches[1])) )
    # END OF GETTING DATA



    # sort the list of coordinates by x-coordinate:
    coord_list = sorted(coord_list, key = lambda x: x[0])


    # Calculating the integral by trapezoid formula:
    integral = 0.0
    for i in range(1, len(coord_list)):
        integral += trapezoid_formula(coord_list[i-1], coord_list[i])


    return integral, n, a, b, coord_list
        



def integral_by_formula():
    """
    Calculates the integral by formula from formula.txt
    """

    # Get the data from formula.txt file: 
    n = 0
    a = b = 0.0
    formula = ""

    with open('formula.txt', 'r') as f:
        f.seek(0)
        lines = f.readlines()

        for i, line in enumerate(lines):
            # finds the value of n
            match_n = re.search(r'n\s*=\s*', line)
            if match_n != None:
                value = re.findall(r'[\d]+', line)
                n = int(value[0])

            # finds value of a
            match_a = re.search(r'a\s*=\s*', line)
            if match_a != None:
                value = re.findall(r'[\d.-]+', line)
                a = float(value[0])

            # finds value of b
            match_b = re.search(r'b\s*=\s*', line)
            if match_b != None:
                value = re.findall(r'[\d.-]+', line)
                b = float(value[0])
            
            # finds the formula expression
            match_formula = re.search(r'f.x.\s*=\s*', line)
            if match_formula != None:
                i1, i2 = match_formula.span()
                value = line[i2:]
                if value[-1] == '\n':
                    value = value[:-1]

                formula = str(value)
    # END OFGETTING DATA

    formula = remove_spaces(formula)
    # Create the coord_list with (2*n + 1) coordinates:

    coord_list = []
    h = (b - a) / float(2*n)

    for i in range(2*n):
        x_coord = float(a + i*h)
        y_coord = float(calculate(formula, x_coord))
        coord_list.append((x_coord, y_coord))
    
    x_last_coord = b
    y_last_coord = float(calculate(formula, x_last_coord))
    coord_list.append((x_last_coord, y_last_coord))

    # Calculate the integral:
    integral = 0.0
    
    integral += coord_list[0][1]

    for i in range(1, n+1):
        integral += 4 * coord_list[2*i - 1][1]

    for i in range(1, n):
        integral += 2 * coord_list[2*i][1]

    integral += coord_list[2*n][1]
    
    integral = h/3 * integral


    return integral, n, a, b, coord_list





def write_to_file(integral, n, a, b, coord_list, checker):
    """
    Writes the value of integral in result.txt
    """
    # clear the file:
    with open("result.txt", 'w') as f:
        f.write('')
    if checker:
        # add info about result in the file:
        with open("result.txt", 'a+') as f:
            f.write("Results\n\n")
            f.write(f"n = {n}, a = {a}, b = {b}\n")
            f.write("\n")
            if (coord_list[0][0] != a) or (coord_list[-1][0] != b):
                f.write("There aren't both coordinates with x-values of a and b in the coordinates.txt file!\n")

            f.write(f"The integral is calculated from {coord_list[0][0]} to {coord_list[-1][0]}.\n")

            f.write(f"\nThe value of integral is {round(integral, 6)}\n\n")

            # also write the coordinates, based on which integral was calculated:
            f.write(f"{len(coord_list)} coordinates:\n\n")

            max_len = max(list(map(lambda x: len(str(round(x[0], 6))), coord_list)))
            max_len = max_len + len(str(len(coord_list)))

            for i in range(len(coord_list)):
                coord_list[i] = (round(coord_list[i][0], 6), round(coord_list[i][1], 6))
                f.write(str(f"x{i} = {coord_list[i][0]}" + 
                    (max_len - len(str(coord_list[i][0])) - len(str(i)) + 1)*" " + f"  y{i} = {coord_list[i][1]}\n"))
    else:
        # Write the messege about program error
        with open("result.txt", 'a+') as f:
            f.write("Something went wrong...\n")
            f.write("Please, check that the input data is correct.")




if __name__ == '__main__':

    integral = 0.0
    a = b = 0.0
    n = 0
    coord_list = []

    choice = users_choice()
    
    try:
        if choice == 1:
            integral, n, a, b, coord_list = integral_by_coordinates()
            if (coord_list[0][0] != a) or (coord_list[-1][0] != b):
                print("There aren't both coordinates with x-values of a and b!")

            print(f"\nThe integral is calculated from {coord_list[0][0]} to {coord_list[-1][0]}.")
            print(f"The value of integral is {round(integral, 6)}")
        else:
            integral, n, a, b, coord_list = integral_by_formula()

            print(f"\nThe integral is calculated from {coord_list[0][0]} to {coord_list[-1][0]}.")
            print(f"The value of integral is {round(integral, 6)}")


        write_to_file(integral, n, a, b, coord_list, True)
    except:
        print('\nSomething went wrong.. Maybe incorrect input...')
        write_to_file(integral, n, a, b, coord_list, False)