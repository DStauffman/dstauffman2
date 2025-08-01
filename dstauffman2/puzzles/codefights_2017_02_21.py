r"""Codefight challenge (digitSumInverse), 2017-02-21, by DStauffman."""

# %% Imports
import doctest
import unittest


# %% Functions - digit_sum
def digit_sum(num):
    out = 0
    while num > 0:
        out += num % 10
        num //= 10
    return out


# %% Functions - brute_force
def brute_force(sum_, num_len):
    out = 0
    for i in range(10**num_len):
        this_sum = digit_sum(i)
        if this_sum == sum_:
            out += 1
            print(i)
    return out


# %% Functions - digitSumInverse
def digitSumInverse(sum_, num_len):
    r"""
    Given integers `sum_` and `num_len`, find the number of non-negative integers less than 10^num_len
    such that the sum of digits for each of them is equal to `sum_`.
    """
    # checks
    assert 0 <= sum_ <= 1000
    assert 1 <= num_len <= 15

    # find simple solutions
    if num_len <= 1:
        return 1 if sum_ < 10 else 0

    # checks for no possible solutions
    if sum_ > 9 * num_len:
        return 0

    # otherwise, solve recursively
    out = 0
    for digit in range(10):
        if digit <= sum_:
            out += digitSumInverse(sum_ - digit, num_len - 1)
    return out


# %% Tests - stringsRearrangement
class Test_stringsRearrangement(unittest.TestCase):
    r"""
    Tests the stringsRearrangement function with the following cases:
        TBD
    """

    def test_1(self):
        self.assertEqual(digitSumInverse(5, 2), 6)

    def test_2(self):
        self.assertEqual(digitSumInverse(0, 2), 1)

    def test_3a(self):
        digits = 10
        self.assertEqual(digitSumInverse(9 * digits, digits), 1)

    def test_3b(self):
        self.assertEqual(digitSumInverse(90, 10), 1)

    def test_4(self):
        self.assertEqual(digitSumInverse(100, 10), 0)

    def test_5(self):
        self.assertEqual(digitSumInverse(23, 3), 15)

    def test_6(self):
        self.assertEqual(digitSumInverse(23, 4), 480)

    def test_7(self):
        self.assertEqual(digitSumInverse(18, 5), 4840)


# %% Script
if __name__ == "__main__":
    # execute unit tests
    unittest.main(exit=False)
    # execute doctests
    doctest.testmod(verbose=False)
