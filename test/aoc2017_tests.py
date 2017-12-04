from unittest import TestCase

from src import d01, d02, d03, d04


class Test_d01(TestCase):
    def test_run(self):
        self.assertEqual(d01.run("1122"), 3)
        self.assertEqual(d01.run("1111"), 4)
        self.assertEqual(d01.run("1234"), 0)
        self.assertEqual(d01.run("91212129"), 9)

        self.assertEqual(d01.run("1212", True), 6)
        self.assertEqual(d01.run("1221", True), 0)
        self.assertEqual(d01.run("123425", True), 4)
        self.assertEqual(d01.run("123123", True), 12)
        self.assertEqual(d01.run("12131415", True), 4)


class Test_d02(TestCase):
    def test_row_checksum(self):
        self.assertEqual(d02.row_checksum("5 1 9 5"), 8)
        self.assertEqual(d02.row_checksum("7 5 3"), 4)
        self.assertEqual(d02.row_checksum("2 4 6 8"), 6)

    def test_run(self):
        inp = """5 1 9 5
7 5 3
2 4 6 8"""
        self.assertEqual(d02.run(inp), 18)

    def test_run_2(self):
        inp = """5 9 2 8
9 4 7 3
3 8 6 5"""
        self.assertEqual(d02.run(inp, True), 9)

    def test_row_even_div_val(self):
        self.assertEqual(d02.row_even_div_val("5 9 2 8"), 4)
        self.assertEqual(d02.row_even_div_val("9 4 7 3"), 3)
        self.assertEqual(d02.row_even_div_val("3 8 6 5"), 2)


class Test_d03(TestCase):
    def test_run(self):
        self.assertEqual(d03.run(12), 3)
        self.assertEqual(d03.run(23), 2)
        self.assertEqual(d03.run(1024), 31)

    def test_spiral_step(self):
        res = []
        i = 1
        for x, y in d03.spiral_step():

            print("{}, {}".format(x, y))
            res.append((x, y))
            if i == 9:
                break
            else:
                i +=1

        cmp = [(0,0),
               (1, 0),
               (1,1),
               (0,1),
               (-1,1),
               (-1,0),
               (-1,-1),
               (0,-1),
               (1,-1)]
        self.assertListEqual(res, cmp)

    def test_run2(self):
        self.assertEqual(d03.run_2(3), 4)
        self.assertEqual(d03.run_2(21), 23)
        self.assertEqual(d03.run_2(145), 147)


class Test_d04(TestCase):
    def test_is_valid_phrase(self):
        self.assertEqual(d04.is_valid_phrase("aa bb cc dd ee"), True)
        self.assertEqual(d04.is_valid_phrase("aa bb cc dd aa"), False)
        self.assertEqual(d04.is_valid_phrase("aa bb cc dd aaa"), True)

    def test_run_1(self):
        inp = """aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa"""
        self.assertEqual(d04.run_1(inp), 2)

    def test_is_anagram_free(self):
        self.assertEqual(d04.is_anagram_free("abcde fghij"), True)
        self.assertEqual(d04.is_anagram_free("abcde xyz ecdab"), False)
        self.assertEqual(d04.is_anagram_free("a ab abc abd abf abj"), True)
        self.assertEqual(d04.is_anagram_free("iiii oiii ooii oooi oooo"), True)
        self.assertEqual(d04.is_anagram_free("oiii ioii iioi iiio"), False)

    def test_run_2(self):
        inp = """abcde fghij
        abcde xyz ecdab
        a ab abc abd abf abj
        iiii oiii ooii oooi oooo
        oiii ioii iioi iiio"""
        self.assertEqual(d04.run_2(inp), 3)
