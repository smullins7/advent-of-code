def c_to_b(c):
    return format(int(c, 16), "0>4b")


def bin_to_int(b):
    return int(b, 2)

def hex_to_int(s):
    return int(s, 16)