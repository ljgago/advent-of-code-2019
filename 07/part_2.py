#! /usr/bin/env python3

# --- Day 7: Amplification Circuit --- Part Two ---
#
# It's no good - in this configuration, the amplifiers can't generate a large
# enough output signal to produce the thrust you'll need. The Elves quickly
# talk you through rewiring the amplifiers into a feedback loop:
#
#       O-------O  O-------O  O-------O  O-------O  O-------O
# 0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
#    |  O-------O  O-------O  O-------O  O-------O  O-------O |
#    |                                                        |
#    '--------------------------------------------------------+
#                                                             |
#                                                             v
#                                                      (to thrusters)
#
# Most of the amplifiers are connected as they were before; amplifier A's output
# is connected to amplifier B's input, and so on. However, the output from
# amplifier E is now connected into amplifier A's input. This creates the
# feedback loop: the signal will be sent through the amplifiers many times.
#
# In feedback loop mode, the amplifiers need totally different phase settings:
# integers from 5 to 9, again each used exactly once. These settings will cause
# the Amplifier Controller Software to repeatedly take input and produce output
# many times before halting. Provide each amplifier its phase setting at its
# first input instruction; all further input/output instructions are for signals.
#
# Don't restart the Amplifier Controller Software on any amplifier during this
# process. Each one should continue receiving and sending signals until it
# halts.
#
# All signals sent or received in this process will be between pairs of
# amplifiers except the very first signal and the very last signal. To start the
# process, a 0 signal is sent to amplifier A's input exactly once.
#
# Eventually, the software on the amplifiers will halt after they have processed
# the final loop. When this happens, the last output signal from amplifier E is
# sent to the thrusters. Your job is to find the largest output signal that can
# be sent to the thrusters using the new phase settings and feedback loop
# arrangement.
#
# Here are some example programs:
#
#   - Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):
#
#     3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
#     27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
#
#   - Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):
#
#     3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
#     -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
#     53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
#
# Try every combination of the new phase settings on the amplifier feedback
# loop. What is the highest signal that can be sent to the thrusters?

from itertools import permutations

def intcode(raw_code, phase, amp):
    ip = 0
    i = 0
    output = 0
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
            if i == 0:
                data = phase
            else:
                data = amp[0]
            code[code[ip+1]] = data
            i += 1
            ip += 2
        elif opcode == 4:
            output = param1
            yield output
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
            yield output
            return

def amp_array(raw_code, phase, gain):
    amp = gain
    feedback = 0
    best_amp = 0
    while feedback < 1000:
        for p in phase:
            amp = intcode(raw_code, p, amp)
        if amp > best_amp:
            best_amp = amp
        feedback += 1
    return best_amp


def amp_feedback(raw_code, phase, gain):
    amp = [gain]
    A = intcode(raw_code, phase[0], amp)
    B = intcode(raw_code, phase[1], amp)
    C = intcode(raw_code, phase[2], amp)
    D = intcode(raw_code, phase[3], amp)
    E = intcode(raw_code, phase[4], amp)
    in_A = in_B = in_C = in_D = in_E = 0
    while True:
        try:
            in_B = next(A)
            amp.clear()
            amp.append(in_B)
        except:
            pass
        try:
            in_C = next(B)
            amp.clear()
            amp.append(in_C)
        except:
            pass
        try:
            in_D = next(C)
            amp.clear()
            amp.append(in_D)
        except:
            pass
        try:
            in_E = next(D)
            amp.clear()
            amp.append(in_E)
        except:
            pass
        try:
            in_A = next(E)
            amp.clear()
            amp.append(in_A)
        except:
            #print(in_A)
            return in_A

def best_amp_phase(raw_code, perm):
    best_amp = 0
    best_phase = 0
    amp = 0
    for phase in list(perm):
        amp = amp_feedback(raw_code, phase, 0)
        if amp > best_amp:
            best_amp, best_phase = amp, phase
    return (best_amp, best_phase)

def test():
    assert amp_feedback([3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
                         27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5],
                        [9, 8, 7, 6, 5], 0) == 139629729, "Should be 139629729"
    assert amp_feedback([3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55,
                         1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008,
                         54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1,
                         56, 1005, 56, 6, 99, 0, 0, 0, 0, 10],
                        [9, 7, 8, 5, 6], 0) == 18216, "Should be 18216"

filename = open("d7input.txt", "r")
input_data_str = filename.readline()
input_data = list(map(int, input_data_str.split(",")))
perm_tuple = permutations([5, 6, 7, 8, 9])
best = best_amp_phase(input_data, perm_tuple)
print("The best Amp-Phase:", best)
# print(intcode(input_data))
# test()
