#!/usr/bin/env sage

n = 65536

first_num = 61679
second_num = 10744

seed = b = Mod(first_num, n)
next_seed = Mod(second_num, n)

a = (next_seed - b) / seed

def gen_seed(seed):
    return b + a * seed
