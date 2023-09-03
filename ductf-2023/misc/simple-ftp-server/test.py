#!/usr/bin/env python3

import operator

FLAG = "abcd"


class A:
    def __init__(self):
        pass

    def cmd(self, cmd, args=None):
        f = operator.attrgetter(cmd)(self)
        if args is not None:
            print(f(args))
        else:
            print(f())

    def help():
        print("help")


a = A()
