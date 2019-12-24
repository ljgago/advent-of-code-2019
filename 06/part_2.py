#! /usr/bin/env python3

# --- Day 6: Universal Orbit Map --- Part Two ---
#
# Now, you just need to figure out how many orbital transfers you (YOU) need to
# take to get to Santa (SAN).
#
# You start at the object YOU are orbiting; your destination is the object SAN
# is orbiting. An orbital transfer lets you move from any object to an object
# orbiting or orbited by that object.
#
# For example, suppose you have the following map:
#
# COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
# K)YOU
# I)SAN
#
# Visually, the above map of orbits looks like this:
#
#                           YOU
#                          /
#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I - SAN
#
# In this example, YOU are in orbit around K, and SAN is in orbit around I. To
# move from K to I, a minimum of 4 orbital transfers are required:
#
#     K to J
#     J to E
#     E to D
#     D to I
#
# Afterward, the map of orbits looks like this:
#
#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I - SAN
#                  \
#                   YOU
#
# What is the minimum number of orbital transfers required to move from the
# object YOU are orbiting to the object SAN is orbiting? (Between the objects
# they are orbiting - not between YOU and SAN.)

def get_intersection_distance(vec1, vec2):
    dist1 = 0
    dist2 = 0
    for data1 in vec1:
        for data2 in vec2:
            if data1 == data2:
                return data1, dist1 + dist2
            dist2 += 1
        dist1 += 1
        dist2 = 0
    return 0, 0

def orbit_count_distance(map_data, you, san):
    you_distance = []
    san_distance = []
    data = you
    while data != None:
        data = map_data.get(data)
        if data != None:
            you_distance.append(data)
    data = san
    while data != None:
        data = map_data.get(data)
        if data != None:
            san_distance.append(data)
    return get_intersection_distance(you_distance, san_distance)

filename = open("d6input.txt", "r")
input_data_str = filename.read()
input_data = dict(x.split(")")[::-1] for x in map(str, input_data_str.splitlines()))
planet, distance = orbit_count_distance(input_data, "YOU", "SAN")
print("Intersection Planet:", planet)
print("Distance:", distance)

# List Comprehension
# Dictionary data (I can't use this because only I have one key an the center
# of mass are repeated)
# input_data = dict(x.split(")") for x in map(str, input_data_str.splitlines()))
#
# Dictionary data in reverse mode
# input_data = dict(x.split(")")[::-1] for x in map(str, input_data_str.splitlines()))
