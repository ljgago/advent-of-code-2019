#! /usr/bin/env python3

from vector_2d import Vector

directions = {
    'R': Vector(0, 1), 'L': Vector(0, -1),
    'U': Vector(1, 0), 'D': Vector(-1, 0),
}

def graph_from_turns(line):
    turns = [
        (directions[direction_letter], int(''.join(magnitude)))
        for [direction_letter, *magnitude] in line.split(',')
    ]
    graph = set()
    central = cursor = Vector(0, 0)
    for direction, magnitude in turns:
        graph.update({direction * step + cursor for step in range(0, magnitude)})
        cursor += direction * magnitude
    return graph

with open("input") as f:
    [a, b] = [graph_from_turns(line) for line in f]
    collisions = a.intersection(b)
    print(sorted([abs(v.x) + abs(v.y) for v in collisions])[1])
