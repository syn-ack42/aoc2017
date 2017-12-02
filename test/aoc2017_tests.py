from unittest import TestCase

from src import d01, d02


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