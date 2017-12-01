import argparse


def run(inp, q2=False):
    res = 0
    off = 1
    l = len(inp)

    if q2:
        off = int(l/2)

    for i in range(0, l):
        if inp[i] == inp[(i + off) % l]:
            res += int(inp[i])

    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q2", "-2", help="question 2", action="store_true")
    parser.add_argument("input", help="puzzle input", nargs=1)
    args = parser.parse_args()

    answer = run(args.input[0], args.q2)
    print("answer: {}".format(answer))


if __name__ == '__main__':
    main()
