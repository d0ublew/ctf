#!/usr/bin/env python3

class Foo(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


foo = Foo("bar", "baz", "leet")
user_controlled_data = input("Input: ")

# `0` here is a placeholder for the first argument in `.format()`
combined = ("{0.a} " + user_controlled_data + " {0.b}").format(foo)
print(combined)

# the above is equivalent to this, which means we could create our own format
# template inside `user_controlled_data`
template = "{0.a} " + user_controlled_data + " {0.b}"
print("template = " + template)
combined = template.format(foo)
print(combined)
