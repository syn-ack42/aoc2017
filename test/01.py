from unittest import TestCase
from src import d01

class TestRun(TestCase):
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
