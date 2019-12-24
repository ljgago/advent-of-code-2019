#! /usr/bin/env python3

# --- Day 3: Crossed Wires --- Part Two ---
#
# It turns out that this circuit is very timing-sensitive; you actually need to
# minimize the signal delay.
#
# To do this, calculate the number of steps each wire takes to reach each
# intersection; choose the intersection where the sum of both wires' steps is
# lowest. If a wire visits a position on the grid multiple times, use the steps
# value from the first time it visits that position when calculating the total
# value of a specific intersection.
#
# The number of steps a wire takes is the total number of grid squares the wire
# has entered to get to that location, including the intersection being
# considered. Again consider the example from above:
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
# In the above example, the intersection closest to the central port is reached
# after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second
# wire for a total of 20+20 = 40 steps.
#
# However, the top-right intersection is better: the first wire takes only
# 8+5+2 = 15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30
# steps.
#
# Here are the best steps for the extra examples from above:
#
#     R75,D30,R83,U83,L12,D49,R71,U7,L72
#     U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
#     R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
#     U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps
#
# What is the fewest combined steps the wires must take to reach an
# intersection?

input_wire1_test = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
input_wire2_test = "U62,R66,U55,R34,D71,R55,D58,R83"

input_wire3_test = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
input_wire4_test = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"

input = open("input", "r")
input_wire1 = input.readline()
input_wire2 = input.readline()
print(input_wire1)
print(input_wire2)

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

def best_step(intersection_points, input1, input2):
    step = -1
    for intersection_point in intersection_points:
        step1 = 0
        step2 = 0
        for i, point in enumerate(input1):
            if point == intersection_point:
                step1 = i
                break
        for i, point in enumerate(input2):
            if point == intersection_point:
                step2 = i
                break
        if step > (step1 + step2):
            step = step1 + step2
        elif step < 0:
            step = step1 + step2
        else:
            continue
    return step


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
    print("Min Distance:")
    print(min_distance)

    step = best_step(intersection[1:], points_wire1, points_wire2)
    print("Best step:")
    print(step)

calcule(input_wire1, input_wire2)
