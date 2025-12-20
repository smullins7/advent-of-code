import math


def c_to_b(c):
    return format(int(c, 16), "0>4b")


def bin_to_int(b):
    return int(b, 2)


def int_to_bin(i, padding=0):
    return (bin(i)[2:]).zfill(padding)


def hex_to_int(s):
    return int(s, 16)


def digits(n: int) -> int:
    return int(math.log10(n)) + 1
