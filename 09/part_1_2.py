#! /usr/bin/env python3

# --- Day 9: Sensor Boost ---
#
# You've just said goodbye to the rebooted rover and left Mars when you receive
# a faint distress signal coming from the asteroid belt. It must be the Ceres
# monitoring station!
#
# In order to lock on to the signal, you'll need to boost your sensors. The
# Elves send up the latest BOOST program - Basic Operation Of System Test.
#
# While BOOST (your puzzle input) is capable of boosting your sensors, for
# tenuous safety reasons, it refuses to do so until the computer it runs on
# passes some checks to demonstrate it is a complete Intcode computer.
#
# Your existing Intcode computer is missing one key feature: it needs support
# for parameters in relative mode.
#
# Parameters in mode 2, relative mode, behave very similarly to parameters in
# position mode: the parameter is interpreted as a position. Like position mode,
# parameters in relative mode can be read from or written to.
#
# The important difference is that relative mode parameters don't count from
# address 0. Instead, they count from a value called the relative base. The
# relative base starts at 0.
#
# The address a relative mode parameter refers to is itself plus the current
# relative base. When the relative base is 0, relative mode parameters and
# position mode parameters with the same value refer to the same address.
#
# For example, given a relative base of 50, a relative mode parameter of -7
# refers to memory address 50 + -7 = 43.
#
# The relative base is modified with the relative base offset instruction:
#
#   - Opcode 9 adjusts the relative base by the value of its only parameter. The
#     relative base increases (or decreases, if the value is negative) by the
#     value of the parameter.
#
# For example, if the relative base is 2000, then after the instruction 109,19,
# the relative base would be 2019. If the next instruction were 204,-34, then
# the value at address 1985 would be output.
#
# Your Intcode computer will also need a few other capabilities:
#
#   - The computer's available memory should be much larger than the initial
#     program. Memory beyond the initial program starts with the value 0 and can
#     be read or written like any other memory. (It is invalid to try to access
#     memory at a negative address, though.)
#   - The computer should have support for large numbers. Some instructions near
#     the beginning of the BOOST program will verify this capability.
#
# Here are some example programs that use these features:
#
#   - 109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 takes no input
#     and produces a copy of itself as output.
#   - 1102,34915192,34915192,7,4,7,99,0 should output a 16-digit number.
#   - 104,1125899906842624,99 should output the large number in the middle.
#
# The BOOST program will ask for a single input; run it in test mode by
# providing it the value 1. It will perform a series of checks on each opcode,
# output any opcodes (and the associated parameter modes) that seem to be
# functioning incorrectly, and finally output a BOOST keycode.
#
# Once your Intcode computer is fully functional, the BOOST program should
# report no malfunctioning opcodes when run in test mode; it should only output
# a single value, the BOOST keycode. What BOOST keycode does it produce?
#
# --- Part Two ---
#
# You now have a complete Intcode computer.
#
# Finally, you can lock on to the Ceres distress signal! You just need to boost
# your sensors using the BOOST program.
#
# The program runs in sensor boost mode by providing the input instruction the
# value 2. Once run, it will boost the sensors automatically, but it might take
# a few seconds to complete the operation on slower hardware. In sensor boost
# mode, the program will output a single value: the coordinates of the distress
# signal.
#
# Run the BOOST program in sensor boost mode. What are the coordinates of the
# distress signal?

def intcode(raw_code):
    ip = 0
    output = []
    code = raw_code.copy()
    code = code + [0]*300
    base = 0
    while ip < len(code):
        opcode = code[ip] % 100
        modes = int(str(code[ip] // 100), 16)
        param1_addr = 0
        param2_addr = 0
        param3_addr = 0
        # mode 0x0 == 0x0
        # mode 0x10 ==
        try:
            if modes & 0x1:
                param1_addr = ip+1
            elif modes & 0x2:
                param1_addr = base + code[ip+1]
            else:
                param1_addr = code[ip+1]
        except:
            param1_addr = 0
        try:
            if modes & 0x10:
                param2_addr = ip+2
            elif modes & 0x20:
                param2_addr = base + code[ip+2]
            else:
                param2_addr = code[ip+2]
        except:
            param2_addr = 0
        try:
            if modes & 0x100:
                param3_addr = ip+3
            elif modes & 0x200:
                param3_addr = base + code[ip+3]
            else:
                param3_addr = code[ip+3]
        except:
            param3_addr = 0

        # print("IP :", ip)
        # print("Param 1 :", param1)
        # print("Param 2 :", param2)
        # print("Param 3 :", param3)

        if opcode == 1:
            code[param3_addr] = code[param1_addr] + code[param2_addr]
            ip += 4
        elif opcode == 2:
            code[param3_addr] = code[param1_addr] * code[param2_addr]
            ip += 4
        elif opcode == 3:
            data = input()
            if data.isdigit():
                try:
                    code[param1_addr] = int(data)
                except:
                    param1_addr = 0
            else:
                print("Unknown code")
                return
            ip += 2
        elif opcode == 4:
            output.append(code[param1_addr])
            ip += 2
        elif opcode == 5:
            if code[param1_addr] != 0:
                ip = code[param2_addr]
            else:
                ip += 3
        elif opcode == 6:
            if code[param1_addr] == 0:
                ip = code[param2_addr]
            else:
                ip += 3
        elif opcode == 7:
            if code[param1_addr] < code[param2_addr]:
                code[param3_addr] = 1
            else:
                code[param3_addr] = 0
            ip += 4
        elif opcode == 8:
            if code[param1_addr] == code[param2_addr]:
                code[param3_addr] = 1
            else:
                code[param3_addr] = 0
            ip += 4
        elif opcode == 9:
            base += code[param1_addr]
            ip += 2
        elif opcode == 99:
            return output

def intcode_test():
    assert intcode([109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]) == [
        109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99], "Should be equal"
    print(intcode([109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]))
    print(intcode([1102, 34915192, 34915192, 7, 4, 7, 99, 0]))
    print(intcode([104, 1125899906842624, 99]))

filename = open("d9input.txt", "r")
input_data_str = filename.read()
input_data = list(map(int, input_data_str.split(",")))
print("Enter code:")
print(intcode(input_data))
#intcode_test()
