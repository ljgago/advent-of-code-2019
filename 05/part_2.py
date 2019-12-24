#! /usr/bin/env python3

# --- Day 5: Sunny with a Chance of Asteroids --- Part Two ---
# 
# The air conditioner comes online! Its cold air feels good for a while, but
# then the TEST alarms start to go off. Since the air conditioner can't vent
# its heat anywhere but back into the spacecraft, it's actually making the air
# inside the ship warmer.
#
# Instead, you'll need to use the TEST to extend the thermal radiators.
# Fortunately, the diagnostic program (your puzzle input) is already equipped
# for this. Unfortunately, your Intcode computer is not.
#
# Your computer is only missing a few opcodes:
#
# - Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the
#   instruction pointer to the value from the second parameter. Otherwise, it
#   does nothing.
# - Opcode 6 is jump-if-false: if the first parameter is zero, it sets the
#   instruction pointer to the value from the second parameter. Otherwise, it
#   does nothing.
# - Opcode 7 is less than: if the first parameter is less than the second
#   parameter, it stores 1 in the position given by the third parameter. 
#   Otherwise, it stores 0.
# - Opcode 8 is equals: if the first parameter is equal to the second
#   parameter, it stores 1 in the position given by the third parameter.
#   Otherwise, it stores 0.
#
# Like all instructions, these instructions need to support parameter modes as
# described above.
#
# Normally, after an instruction is finished, the instruction pointer increases
# by the number of values in that instruction. However, if the instruction
# modifies the instruction pointer, that value is used and the instruction
# pointer is not automatically increased.
#
# For example, here are several programs that take one input, compare it to the
# value 8, and then produce one output:
#
# - 3,9,8,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input
#   is equal to 8; output 1 (if it is) or 0 (if it is not).
# - 3,9,7,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input
#   is less than 8; output 1 (if it is) or 0 (if it is not).
# - 3,3,1108,-1,8,3,4,3,99 - Using immediate mode, consider whether the input
#   is equal to 8; output 1 (if it is) or 0 (if it is not).
# - 3,3,1107,-1,8,3,4,3,99 - Using immediate mode, consider whether the input
#   is less than 8; output 1 (if it is) or 0 (if it is not).
#
# Here are some jump tests that take an input, then output 0 if the input was
# zero or 1 if the input was non-zero:
#
# - 3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 (using position mode)
# - 3,3,1105,-1,9,1101,0,0,12,4,12,99,1 (using immediate mode)
#
# Here's a larger example:
#
# 3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
# 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
# 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
#
# The above example program uses an input instruction to ask for a single
# number. The program will then output 999 if the input value is below 8,
# output 1000 if the input value is equal to 8, or output 1001 if the input
# value is greater than 8.
#
# This time, when the TEST diagnostic program runs its input instruction to get
# the ID of the system to test, provide it 5, the ID for the ship's thermal
# radiator controller. This diagnostic test suite only outputs one number, the
# diagnostic code.
#
# What is the diagnostic code for system ID 5?

def intcode(raw_code):
    ip = 0
    output = []
    code = raw_code.copy()
    while ip < len(code):
        opcode = code[ip] % 100
        modes = int(str(code[ip] // 100), 2)
        param1 = 0
        param2 = 0
        param3 = 0

        if modes & 1:
            try:
                param1 = code[ip+1]
            except:
                param1 = 0
        else:
            try:
                param1 = code[code[ip+1]]
            except:
                param1 = 0
        if modes & 2:
            try:
                param2 = code[ip+2]
            except:
                param2 = 0
        else:
            try:
                param2 = code[code[ip+2]]
            except:
                param2 = 0
        try:
            param3 = code[ip+3]
        except:
            param3 = 0

        # print("Param 1 :", param1)
        # print("Param 2 :", param2)
        # print("Param 3 :", param3)

        if opcode == 1:
            code[param3] = param1 + param2
            ip += 4
        elif opcode == 2:
            code[param3] = param1 * param2
            ip += 4
        elif opcode == 3:
            data = input()
            if data.isdigit():
                code[code[ip+1]] = int(data)
            else:
                print("Unknown code")
                return
            ip += 2
        elif opcode == 4:
            output.append(param1)
            ip += 2
        elif opcode == 5:
            if param1 != 0:
                ip = param2
            else:
                ip += 3
        elif opcode == 6:
            if param1 == 0:
                ip = param2
            else:
                ip += 3
        elif opcode == 7:
            if param1 < param2:
                code[param3] = 1
            else:
                code[param3] = 0
            ip += 4
        elif opcode == 8:
            if param1 == param2:
                code[param3] = 1
            else:
                code[param3] = 0
            ip += 4
        elif opcode == 99:
            return output

def intcode_test():
    print("Enter number minor to 8 (< 8):")
    assert intcode([ 3,9,8,9,10,9,4,9,99,-1,8 ]) == [0], "Should be 0"
    print("Enter number equal to 8 (= 8):")
    assert intcode([ 3,9,8,9,10,9,4,9,99,-1,8 ]) == [1], "Should be 1"
    print("Enter number major to 8 (> 8):")
    assert intcode([ 3,9,8,9,10,9,4,9,99,-1,8 ]) == [0], "Should be 0"

    print("Enter number minor to 8 (< 8):")
    assert intcode([ 3,9,7,9,10,9,4,9,99,-1,8 ]) == [1], "Should be 1"
    print("Enter number major or equal to 8 (>= 8):")
    assert intcode([ 3,9,7,9,10,9,4,9,99,-1,8 ]) == [0], "Should be 0"

    print("Enter number minor to 8 (< 8):")
    assert intcode([ 3,3,1108,-1,8,3,4,3,99 ]) == [0], "Should be 0"
    print("Enter number equal to 8 (= 8):")
    assert intcode([ 3,3,1108,-1,8,3,4, 3,99 ]) == [1], "Should be 1"
    print("Enter number major to 8 (> 8):")
    assert intcode([ 3,3,1108,-1,8,3,4,3,99 ]) == [0], "Should be 0"

    print("Enter number minor to 8 (< 8):")
    assert intcode([ 3,3,1107,-1,8,3,4,3,99 ]) == [1], "Should be 1"
    print("Enter number major or equal to 8 (>= 8):")
    assert intcode([ 3,3,1107,-1,8,3,4,3,99 ]) == [0], "Should be 0"

    data = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,
        0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,
        1105,1,46,98,99
    ]
    print("Enter number minor to 8 (< 8):")
    assert intcode(data) == [999], "Should be 999"
    print("Enter number equal to 8 (= 8):")
    assert intcode(data) == [1000], "Should be 1000"
    print("Enter number major to 8 (> 8):")
    assert intcode(data) == [1001], "Should be 1001"

filename = open("d5input.txt", "r")
input_data_str = filename.readline()
input_data = list(map(int, input_data_str.split(",")))
print("Enter code:")
# print(intcode(input_data))
intcode_test()
