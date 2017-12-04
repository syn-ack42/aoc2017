import argparse
import time
import importlib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", "-d", help="day")
    parser.add_argument("--q2", "-2", help="question 2", action="store_true")
    parser.add_argument("--input", "-i", help="puzzle input string")
    parser.add_argument("--file", "-f", help="puzzle input file")
    args = parser.parse_args()

    if not args.day:
        print("select a day, dunderhead!")
        exit(1)

    d = str(args.day).rjust(2, "0")

    m = importlib.import_module("d" + d)

    if args.file:
        inp = open(args.file).read()
    elif args.input:
        inp = args.input
    else:
        print("no input, sucker!")
        exit(1)

    if args.q2:
        answer = m.run_2(inp)
    else:
        answer = m.run_1(inp)

    print("answer: {}".format(answer))


if __name__ == '__main__':
    s = time.perf_counter()
    main()
    e = time.perf_counter()
    print("time elapsed: {} s".format(e - s))
