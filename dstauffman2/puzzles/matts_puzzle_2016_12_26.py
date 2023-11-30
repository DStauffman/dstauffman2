"""
Created on Mon Dec 26 12:38:44 2016.

@author: David C. Stauffer

Your input is a (zero indexed) list of numbers.
Your goal is to return any equilibrium index in the list.
An equilibrium index is the location in the list where the sum of all members
to the right is equal to the sum of all members to the left. The data at the index itself
is not included in either sum. The sum of an empty list is considered to be 0.
If no equilibrium index exists, return -1.

Example input:
A = [-1, 3, -4, 5, 1, -6, 2, 1]

Equillibrium Indicies:
I = [1, 3, 7]

Keep in mind you don't need to find all the equilibrium indices, just return any one
of them and the solution is considered correct.

Performance constraints:
Your solution must return the correct answer in less than 0.5 seconds, even for the worst case input.
The worst case input is a list with no equilibrium points and 100,000 members.

So that's it.
Read a list,
Return an equilibrium index or -1 if none exist.
Do it fast.
Don't spend more than 1 hour.
Report your runtime along with your algorithm/code.
"""

# %% Imports
import random

import numpy as np


# %% Functions - find_equilibriums
def find_equilibriums(x):
    r"""Find the equilibrium points."""
    # force input to be array
    x = np.asanyarray(x)

    # build some cumsums from each direction
    cs1 = np.cumsum(x)
    cs2 = np.cumsum(x[::-1])[::-1]

    # calculate results
    y = np.flatnonzero(cs1 == cs2)

    # if empty, return -1 instead
    if y.size == 0:
        y = [-1]
    return y


# %% Functions - boring_version
def boring_version(x, early=False):
    r"""Find the equilibrium points without using NumPy."""
    # initialize output
    y = []

    # build working sums
    s1 = 0
    s2 = sum(x)

    for ix in range(len(x)):
        temp = x[ix]
        s1 += temp
        if s1 == s2:
            y.append(ix)
            if early:
                return y
        s2 -= temp

    # check for empty case
    if not y:
        y.append(-1)
    return y


# %% Script
if __name__ == "__main__":
    A = [-1, 3, -4, 5, 1, -6, 2, 1]
    I1a = boring_version(A)
    I1b = find_equilibriums(A)
    np.testing.assert_array_equal(I1a, I1b)
    print(I1b)

    rand = [random.randint(-5, 5) for x in range(100000)]
    rand2 = np.array(rand)
    I2a = boring_version(rand)
    I2b = find_equilibriums(rand)
    np.testing.assert_array_equal(I2a, I2b)
    print(I2b)

    worst = list(range(100000))
    worst2 = np.array(worst)
    I3a = boring_version(worst)
    I3b = find_equilibriums(worst)
    np.testing.assert_array_equal(I3a, I3b)
    print(I3b)

    """
    %timeit I1  = find_equilibriums(A)
    %timeit I2  = find_equilibriums(rand)
    %timeit I2b = find_equilibriums(rand2)
    %timeit I3  = find_equilibriums(worst)
    %timeit I3b = find_equilibriums(worst2)

    # Approximately 0.00042s (420 microseconds) on my work computer.  Go numpy!
    # Note: takes 6ms if worst input is not already a numpy array

    %timeit I1 = boring_version(A)
    %timeit I2 = boring_version(rand)
    %timeit I3 = boring_version(worst)

    # Approximately 0.0134s (13.4 milliseconds) on my work computer. (32X slower than numpy...)
    """
