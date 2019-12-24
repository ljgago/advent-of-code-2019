#! /usr/bin/env python3

# --- Day 4: Secure Container ---
#
# You arrive at the Venus fuel depot only to discover it's protected by a
# password. The Elves had written the password on a sticky note, but someone
# threw it out.
#
# However, they do remember a few key facts about the password:
#
#     It is a six-digit number.
#     The value is within the range given in your puzzle input.
#     Two adjacent digits are the same (like 22 in 122345).
#     Going from left to right, the digits never decrease; they only ever
#     increase or stay the same (like 111123 or 135679).
#
# Other than the range rule, the following are true:
#
#     111111 meets these criteria (double 11, never decreases).
#     223450 does not meet these criteria (decreasing pair of digits 50).
#     123789 does not meet these criteria (no double).
#
# How many different passwords within the range given in your puzzle input meet
# these criteria?

input_range = [273025, 767253]
input_test = [111111, 223450, 123789, 112233, 123444,
              111122, 222234, 233344, 223334]

def check_rules(password):
    str_password = str(password)
    i = 0
    hasAdjacent = False
    isMinToMax = False
    while i < 5:
        if str_password[i] == str_password[i + 1]:
            hasAdjacent = True
        if str_password[i] <= str_password[i + 1]:
            isMinToMax = True
        else:
            isMinToMax = False
            break
        i += 1
    if hasAdjacent and isMinToMax:
        return True
    else:
        return False

def calculate(passwords):
    count = 0
    for password in range(passwords[0], passwords[1]):
        if check_rules(password):
            count += 1
    return count

def calculate_test(passwords):
    for password in passwords:
        if check_rules(password):
            print(password, True)
        else:
            print(password, False)

# count = calculate_test(input_test)
print("Count:", calculate(input_range))
