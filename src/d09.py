import re
import sys

sys.setrecursionlimit(2000)

def run_1(inp):
    inp = clean_garbage(inp)
    return sum_subscores(inp)

def sum_subscores(inp, level = 1):
    """
    >>> from src import d09
    >>> d09.sum_subscores("{}")
    1
    >>> d09.sum_subscores("{{{}}}")
    6
    >>> d09.sum_subscores("{{},{}}")
    5
    >>> d09.sum_subscores("{{{},{},{{}}}}")
    16
    >>> d09.sum_subscores(d09.clean_garbage("{<a>,<a>,<a>,<a>}"))
    1
    >>> d09.sum_subscores(d09.clean_garbage("{{<ab>},{<ab>},{<ab>},{<ab>}}"))
    9
    >>> d09.sum_subscores(d09.clean_garbage("{{<!!>},{<!!>},{<!!>},{<!!>}}"))
    9
    >>> d09.sum_subscores(d09.clean_garbage("{{<a!>},{<a!>},{<a!>},{<ab>}}"))
    3
    """
    if inp == "{}":
        return level
    elif inp == "{}":
        return level -1
    inp = inp[1:-1]
    subgroups = split_subgroups(inp)
    s = 0
    for g in subgroups:
        s += sum_subscores(g, level + 1)
    return s + level

def split_subgroups(inp):
    subgrps = []
    b_level = 0

    buf = []
    for c in inp:
        if c == "{":
            b_level +=1
        elif c == "}":
            b_level -= 1
        elif (c == ",") and b_level == 0:
            subgrps.append("".join(buf))
            buf = []
            continue
        buf.append(c)
    subgrps.append("".join(buf))

    return subgrps


def clean_garbage(stream, with_count = False):
    """
    >>> from src import d09
    >>> d09.clean_garbage('{<bli>,{OK},{{OK<>2},<bla>,<blub>,{}}}', True)
    ('{{OK},{{OK2},{}}}', 10)
    >>> d09.clean_garbage('{<bli>,{OK},{{OK<random characters>2},<bla>,<blub>,{}}}')
    '{{OK},{{OK2},{}}}'
    >>> d09.clean_garbage('{<bli>,{OK},{{OK<<<<>2},<bla>,<blub>,{}}}')
    '{{OK},{{OK2},{}}}'
    >>> d09.clean_garbage('{<bli>,{OK},{{OK<{!>}>2},<bla>,<blub>,{}}}')
    '{{OK},{{OK2},{}}}'
    >>> d09.clean_garbage('{<bli>,{OK},{{OK<!!>2},<bla>,<blub>,{}}}')
    '{{OK},{{OK2},{}}}'
    >>> d09.clean_garbage('{<bli>,{OK},{{OK<!!!>>2},<bla>,<blub>,{}}}')
    '{{OK},{{OK2},{}}}'
    >>> d09.clean_garbage('{<bli>,{OK},{{OK<{o"i!a,<{i<a>2},<bla>,<blub>,{}}}')
    '{{OK},{{OK2},{}}}'
    """
    in_junk = False
    clean_stream = []
    l_stream = len(stream)
    i = 0
    cnt_garbage = 0
    while i < l_stream:
        c = stream[i]
        if c == "!":
            i += 2
            continue
        if in_junk:
            if c == ">":
                in_junk = False
            else:
                cnt_garbage += 1
        else:
            if c == "<":
                in_junk = True
            else:
                clean_stream.append(c)
        i += 1
    s = "".join(clean_stream)
    s = re.sub(r",,+", ",", s)
    s = re.sub(r",\}", "}", s)
    s = re.sub(r"\{,", "{", s)
    if with_count:
        return s, cnt_garbage
    else:
        return s


def run_2(inp):
    s, c = clean_garbage(inp, True)
    return c
