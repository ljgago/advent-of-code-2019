#! /usr/bin/env python3

# --- Day 4: Secure Container --- Part Two ---
#
# An Elf just remembered one more important detail: the two adjacent matching
# digits are not part of a larger group of matching digits.
#
# Given this additional criterion, but still ignoring the range rule, the
# following are now true:
#
#     112233 meets these criteria because the digits never decrease and all
#         repeated digits are exactly two digits long.
#     123444 no longer meets the criteria (the repeated 44 is part of a larger
#         group of 444).
#     111122 meets the criteria (even though 1 is repeated more than twice, it
#         still contains a double 22).
#
# How many different passwords within the range given in your puzzle input meet
# all of the criteria?

input_range = [273025, 767253]
input_test = [111111, 223450, 123789, 112233, 123444,
              111122, 222234, 233344, 223334, 122333]

def check_rules(password):
    str_password = str(password)
    i = 0
    j = 0
    hasOnly2Adjacent = False
    adjacent = []
    isMinToMax = False
    last_value = str_password[0]
    while i < 5:
        # if str_password[i] == str_password[i + 1]:
        #     hasOnly2Adjacent = True
        #     if i == 1:
        #         if last_value == str_password[i]:
        #             hasOnly2Adjacent = False
        #     if i == 2:
        #         if last_value == str_password[i]:
        #             hasOnly2Adjacent = False
        #     last_value = str_password[i]
        #     # if i != 0:
        #     #     if fist_value != last_value and last_value == str_password[i]:
        #     #         hasAdjacent = False
        #     # last_value = str_password[i]
        #     # if i != 0:
        #     #     if last_value == str_password[i]:
        #     #         hasAdjacent = False
        #     # last_value = str_password[i]

        if str_password[i] <= str_password[i + 1]:
            isMinToMax = True
        else:
            isMinToMax = False
            break
        i += 1

    i = 0
    j = 0
    adj_list = []
    while j < 10:
        for str_num in str_password:
            if str(j) == str_num:
                adj_list.append("1")
            else:
                adj_list.append("0")
        adjacent.append(adj_list)
        adj_list = []
        j += 1
    bin_list = []
    for v in adjacent:
        bin_list.append(int("".join(v), 2))
    for v in bin_list:
        if v == 3 or v == 6 or v == 12 or v == 24 or v == 48:
            hasOnly2Adjacent = True
            break

    if hasOnly2Adjacent and isMinToMax:
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

# print("Count:", calculate(input))

calculate_test(input_test)
# 111111 -> False
# 223450 -> False
# 123789 -> False
# 112233 -> True
# 123444 -> False
# 111122 -> True
# 222234 -> False
# 233344 -> True
# 223334 -> True
# 122333 -> True
