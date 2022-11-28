# testing things
import expression
from expression import *
import main
from main import integral_by_coordinates
import re

# integral_by_coordinates()

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
            value = re.findall(r'[\d.]+', line)
            n = int(value[0])

        # finds value of a
        match_a = re.search(r'a\s*=\s*', line)
        if match_a != None:
            value = re.findall(r'[\d.]+', line)
            a = float(value[0])

        # finds value of b
        match_b = re.search(r'b\s*=\s*', line)
        if match_b != None:
            value = re.findall(r'[\d.]+', line)
            b = float(value[0])

        # find the index of line, which is "Enter coordinates of n points through the space"
        if "coordinates of n points through the space" in line:
            line_ind = i

    coord_list = []
    for line in lines[line_ind:]:
        matches = re.findall(r'[\d.]+', line)
        if len(matches) == 2:
            coord_list.append( (float(matches[0]), float(matches[1])) )


    print(n, a, b)
    print(coord_list)
