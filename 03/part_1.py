#! /usr/bin/env python3

# --- Day 3: Crossed Wires ---
#
# The gravity assist was successful, and you're well on your way to the Venus
# refuelling station. During the rush back on Earth, the fuel management system
# wasn't completely installed, so that's next on the priority list.
#
# Opening the front panel reveals a jumble of wires. Specifically, two wires
# are connected to a central port and extend outward on a grid. You trace the
# path each wire takes as it leaves the central port, one wire per line of
# text (your puzzle input).
#
# The wires twist and turn, but the two wires occasionally cross paths. To fix
# the circuit, you need to find the intersection point closest to the central
# port. Because the wires are on a grid, use the Manhattan distance for this
# measurement. While the wires do technically cross right at the central port
# where they both start, this point does not count, nor does a wire count as
# crossing with itself.
#
# For example, if the first wire's path is R8,U5,L5,D3, then starting from the
# central port (o), it goes right 8, up 5, left 5, and finally down 3:
#
# ...........
# ...........
# ...........
# ....+----+.
# ....|....|.
# ....|....|.
# ....|....|.
# .........|.
# .o-------+.
# ...........
#
# Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6,
# down 4, and left 4:
#
# ...........
# .+-----+...
# .|.....|...
# .|..+--X-+.
# .|..|..|.|.
# .|.-X--+.|.
# .|..|....|.
# .|.......|.
# .o-------+.
# ...........
#
# These wires cross at two locations (marked X), but the lower-left one is
# closer to the central port: its distance is 3 + 3 = 6.
#
# Here are a few more examples:
#
#     R75,D30,R83,U83,L12,D49,R71,U7,L72
#     U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
#     R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
#     U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
#
# What is the Manhattan distance from the central port to the closest intersection?

input_wire1_test = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
input_wire2_test = "U62,R66,U55,R34,D71,R55,D58,R83"

input_wire3_test = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
input_wire4_test = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"

def up(point, value):
    points = []
    for y in range(value):
        points.append((point[0], point[1] + (1 + y)))
    return points

def down(point, value):
    points = []
    for y in range(value):
        points.append((point[0], point[1] - 1 - y))
    return points

def right(point, value):
    points = []
    for x in range(value):
        points.append((point[0] + (1 + x), point[1]))
    return points

def left(point, value):
    points = []
    for x in range(value):
        points.append((point[0] - (1 + x), point[1]))
    return points

def distance_taxicab(origin, destiny):
    return abs(origin[0] - destiny[0]) + abs(origin[1] - destiny[1])

def calcule(input1, input2):
    wire1 = input1.split(",")
    wire2 = input2.split(",")
    # print(wire1)
    points_wire1 = [(0, 0)]
    points_wire2 = [(0, 0)]
    for wire in wire1:
        code = wire[:1]
        last_point = points_wire1[-1]
        move = int(wire[1:])
        new_points = []
        # get the move code
        if code == "U":
            new_points = up(last_point, move)
        elif code == "D":
            new_points = down(last_point, move)
        elif code == "R":
            new_points = right(last_point, move)
        elif code == "L":
            new_points = left(last_point, move)
        else:
            print("Error move code")
        points_wire1 += new_points
    for wire in wire2:
        code = wire[:1]
        last_point = points_wire2[-1]
        move = int(wire[1:])
        new_points = []
        # get the move code
        if code == "U":
            new_points = up(last_point, move)
        elif code == "D":
            new_points = down(last_point, move)
        elif code == "R":
            new_points = right(last_point, move)
        elif code == "L":
            new_points = left(last_point, move)
        else:
            print("Error move code")
        points_wire2 += new_points
    print("wire1:")
    #print(points_wire1)
    print("wire2:")
    #print(points_wire2)

    intersection = []
    for wire1 in points_wire1:
        for wire2 in points_wire2:
            if wire1 == wire2:
                intersection.append(wire1)
    print(intersection)
    origin = (0, 0)
    # calcule the min Manhattan distance
    min_distance = distance_taxicab(origin, intersection[1])
    # for loop without the origin point
    for destiny in intersection[2:]:
        distance = distance_taxicab(origin, destiny)
        if distance < min_distance:
            min_distance = distance
    return min_distance

filename = open("d3input.txt", "r")
input_data_str = filename.readline()
input_data = list(map(int, input_data_str.split(",")))
print("Min Distance:")
print(calcule(input_data[0], input_data[1]))
