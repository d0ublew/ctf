import sys

a = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ" + \
    "[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ "


def arg133(arg432):
    if arg432 == a[38] + a[78] + a[67] + a[89] + a[72] + a[43] + a[75] + a[31] + a[53] + a[50] + \
            a[42] + a[16] + a[77] + a[70] + a[38] + a[71] + a[16] + a[67] + a[15] + a[81] + a[19] + a[39]:
        return True
    else:
        print(
            a[51] +
            a[71] +
            a[64] +
            a[83] +
            a[94] +
            a[79] +
            a[64] +
            a[82] +
            a[82] +
            a[86] +
            a[78] +
            a[81] +
            a[67] +
            a[94] +
            a[72] +
            a[82] +
            a[94] +
            a[72] +
            a[77] +
            a[66] +
            a[78] +
            a[81] +
            a[81] +
            a[68] +
            a[66] +
            a[83])
        sys.exit(0)
        return False


def arg111(arg444):
    return arg122(arg444.decode(), a[62])


def arg232():
    arg282 = input(
        a[47] +
        a[75] +
        a[68] +
        a[64] +
        a[82] +
        a[68] +
        a[94] +
        a[68] +
        a[77] +
        a[83] +
        a[68] +
        a[81] +
        a[94] +
        a[66] +
        a[78] +
        a[81] +
        a[81] +
        a[68] +
        a[66] +
        a[83] +
        a[94] +
        a[16] +
        a[82] +
        a[83] +
        a[94] +
        a[79] +
        a[64] +
        a[82] +
        a[82] +
        a[86] +
        a[78] +
        a[81] +
        a[67] +
        a[94] +
        a[69] +
        a[78] +
        a[81] +
        a[94] +
        a[69] +
        a[75] +
        a[64] +
        a[70] +
        a[25] +
        a[94])

    if arg282 == '':
        print("Password 1 is empty")
        sys.exit(0)

    arg383 = input(
        a[47] +
        a[75] +
        a[68] +
        a[64] +
        a[82] +
        a[68] +
        a[94] +
        a[68] +
        a[77] +
        a[83] +
        a[68] +
        a[81] +
        a[94] +
        a[66] +
        a[78] +
        a[81] +
        a[81] +
        a[68] +
        a[66] +
        a[83] +
        a[94] +
        a[17] +
        a[82] +
        a[83] +
        a[94] +
        a[79] +
        a[64] +
        a[82] +
        a[82] +
        a[86] +
        a[78] +
        a[81] +
        a[67] +
        a[94] +
        a[69] +
        a[78] +
        a[81] +
        a[94] +
        a[69] +
        a[75] +
        a[64] +
        a[70] +
        a[25] +
        a[94])

    if arg383 == '':
        print("Password 2 is empty")
        sys.exit(0)

    if arg282 is not None and arg383 is not None:
        arg888 = arg282 + arg383
        return arg888


def arg137():
    return open('flag.txt.enc', 'rb').read()


def arg112():
    print(
        a[54] +
        a[68] +
        a[75] +
        a[66] +
        a[78] +
        a[76] +
        a[68] +
        a[94] +
        a[65] +
        a[64] +
        a[66] +
        a[74] +
        a[13] +
        a[13] +
        a[13] +
        a[94] +
        a[88] +
        a[78] +
        a[84] +
        a[81] +
        a[94] +
        a[69] +
        a[75] +
        a[64] +
        a[70] +
        a[11] +
        a[94] +
        a[84] +
        a[82] +
        a[68] +
        a[81] +
        a[25])


def arg122(arg432, arg423):
    arg433 = arg423
    i = 0
    while len(arg433) < len(arg432):
        arg433 = arg433 + arg423[i]
        i = (i + 1) % len(arg423)
    return "".join([chr(ord(arg422) ^ ord(arg442))
                   for (arg422, arg442) in zip(arg432, arg433)])


password = a[38] + a[78] + a[67] + a[89] + a[72] + a[43] + a[75] + a[31] + a[53] + a[50] + \
    a[42] + a[16] + a[77] + a[70] + a[38] + a[71] + a[16] + a[67] + a[15] + a[81] + a[19] + a[39]
arg444 = arg137()
# arg432 = arg232()
arg133(password)
arg112()
arg423 = arg111(arg444)
print(arg423)
sys.exit(0)
