def run_1(inp):
    lbuff = inp.splitlines()
    c_valid = 0
    for l in lbuff:
        if is_valid_phrase(l):
            c_valid += 1

    return c_valid


def is_valid_phrase(p):
    """
    >>> is_valid_phrase("aa bb cc dd")
    True
    >>> is_valid_phrase("aa bb cc aa")
    False
    >>> is_valid_phrase("aa bb cc aaaa")
    True
    """
    buf = []
    words = p.split()
    for w in words:
        if w in buf:
            return False
        else:
            buf.append(w)
    return True


def run_2(inp):
    lbuff = inp.splitlines()
    c_valid = 0
    for l in lbuff:
        if is_anagram_free(l):
            c_valid += 1

    return c_valid


def is_anagram_free(p):
    buf = []
    words = [sorted(s) for s in p.split()]

    for w in words:
        if w in buf:
            return False
        else:
            buf.append(w)
    return True
