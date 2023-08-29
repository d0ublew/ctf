#!/usr/bin/env python3

"""
Observation:
- When I tried `SEKAI{` as the input, the value in `mem[21]` decreases from 14
up to 8. To get a checkmark output, `mem[21]` needs to be lower than 0.
This suggests that our flag length is 15.

- When our input character is correct, the memory is reset to its original
value except for `mem[21]`.

- Thus, we could check the individual character by modifying the `mem[21]`
value by adjusting the program accordingly, for example, if we set `mem[21]` to
14, it checks the first input character, `mem[21] = 13` checks the second input
character.
"""


def check(idx, char):
    mem = [120, 121, 56, 32, 107, 89, 77, 103, 78, 73, 126,
           125, 10, 3, 24, 0, 0, 0, 5, 0, 0, idx, 0, 'v', 'x']
    while True:
        mem[19] = mem[17] = mem[16] = mem[15] = mem[20] = mem[22]
        mem[15] = mem[21] + 1

        mem[16] = mem[16] + mem[18] * mem[15]
        mem[15] = 0

        mem[15] = char  # inbox.pop(0)
        mem[20] -= 1
        mem[20] = mem[20] * pow(2, 3)

        while True:
            mem[19] = 1
            mem[22] = mem[20] + 1

            if mem[22] < 0:
                mem[19] = mem[19] * pow(2, max(1, abs(mem[22])))
                mem[22] = 0

            if mem[15] - mem[19] >= 0:
                mem[15] -= mem[19]
                if mem[16] - mem[19] >= 0:
                    mem[16] -= mem[19]
                else:
                    mem[17] += mem[19]
            else:
                if mem[16] - mem[19] >= 0:
                    mem[16] -= mem[19]
                    mem[17] += mem[19]

            mem[20] += 1
            if mem[20] >= 0:
                if mem[17] - mem[mem[21]] != 0:
                    # print(mem[24])
                    return False
                mem[17] = mem[20]
                mem[21] -= 1
                # if mem[21] < 0:
                #     print(mem[23])
                return True
            else:
                continue


flag = bytearray(15)
for i in range(15):
    for c in range(33, 127):  # from comment 0
        correct = check(14 - i, c)
        if correct:
            flag[i] = c
            print(bytes(flag))
            break
