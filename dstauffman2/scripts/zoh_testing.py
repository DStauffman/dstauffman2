"""
Zero order hold comparisons and timing.

Created on Tue Jul 14 11:08:40 2020

@author: DStauffman
"""

# %% Imports
from collections import deque

import numpy as np
from scipy.interpolate import interp1d

from dstauffman import zero_order_hold


# %% Functions
def zero_order_hold_simple(x, xp, yp):
    r"""Zero order hold using lists."""

    def func(x0):
        if x0 <= xp[0]:
            return yp[0]
        if x0 >= xp[-1]:
            return yp[-1]
        k = 0
        while x0 > xp[k]:
            k += 1
        return yp[k - 1]

    if isinstance(x, float):
        return func(x)
    elif isinstance(x, list):
        return [func(x) for x in x]
    elif isinstance(x, np.ndarray):
        return np.asarray([func(x) for x in x])
    else:
        raise TypeError("argument must be float, list, or ndarray")


def zero_order_hold_deque(x, xp, yp):
    r"""Zero order hold using queues instead of lists."""

    def func(x0, xP=deque(xp), yP=deque(yp)):
        if x0 <= xP[0]:
            return yP[0]
        if x0 >= xP[-1]:
            return yP[-1]
        while x0 > xP[0]:
            xP.popleft()  # get rid of default
            y = yP.popleft()  # data as we go.
        return y

    return list(map(func, x))


def zero_order_hold_scipy(x, xp, yp):
    r"""Zero order hold using built-in scipy options."""
    func = interp1d(xp, yp, kind="zero", fill_value="extrapolate", assume_sorted=True)
    return func(x)


def zero_order_hold_numpy(x, xp, yp):
    r"""Zero order hold using non-integer indexing of numpy."""
    ix = np.searchsorted(xp, x, side="right") - 1
    return yp[ix]


# %% Tests
if __name__ == "__main__":
    # Case 1: Subsample high rate data
    xp1 = np.linspace(0.0, 100 * np.pi, 500000)
    yp1 = np.sin(2 * np.pi * xp1)

    x1 = np.arange(0.0, 350.0, 0.1)

    y1_a = zero_order_hold_simple(x1[:100], xp1, yp1)  # don't even try this one with the whole set
    y1_b = zero_order_hold_deque(x1, xp1, yp1)
    y1_c = zero_order_hold_scipy(x1, xp1, yp1)
    y1_d = zero_order_hold_numpy(x1, xp1, yp1)
    y1_e = zero_order_hold(x1, xp1, yp1)

    # Case 2: Supersample low rate discrete events
    xp2 = np.array([0.0, 5000.0, 10000.0, 86400.0])
    yp2 = np.array([0, 1, -2, 0])

    x2 = np.arange(0.0, 86400.0)

    y2_a = zero_order_hold_simple(x2, xp2, yp2)
    y2_b = zero_order_hold_deque(x2, xp2, yp2)
    y2_c = zero_order_hold_scipy(x2, xp2, yp2)
    y2_d = zero_order_hold_numpy(x2, xp2, yp2)
    y2_e = zero_order_hold(x2, xp2, yp2)

    # Comparisons
    np.allclose(y1_c[:100], y1_a, atol=1e-14)
    np.allclose(y1_c, y1_b, atol=1e-14)
    np.allclose(y1_c, y1_d, atol=1e-14)
    np.allclose(y1_c, y1_e, atol=1e-14)
    np.allclose(y2_c, y2_a, atol=1e-14)
    np.allclose(y2_c, y2_b, atol=1e-14)
    np.allclose(y2_c, y2_d, atol=1e-14)
    np.allclose(y2_c, y2_e, atol=1e-14)

    # %timeit zero_order_hold_simple(x1[:100], xp1, yp1)
    # 35 * 132 ms ± 4.91 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    # %timeit zero_order_hold_deque(x1, xp1, yp1)
    # 94.2 ms ± 2.02 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    # %timeit zero_order_hold_scipy(x1, xp1, yp1)
    # 22.1 ms ± 677 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    # %timeit zero_order_hold_numpy(x1, xp1, yp1)
    # 227 µs ± 33.1 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
    # %timeit zero_order_hold(x1, xp1, yp1)
    # 713 µs ± 48.2 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
    # %timeit zero_order_hold(x1, xp1, yp1, assume_sorted=True)
    # 252 µs ± 51.9 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

    # %timeit zero_order_hold_simple(x2, xp2, yp2)
    # 113 ms ± 3.87 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    # %timeit zero_order_hold_deque(x2, xp2, yp2)
    # 21.4 ms ± 594 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    # %timeit zero_order_hold_scipy(x2, xp2, yp2)
    # 1.65 ms ± 42.6 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
    # %timeit zero_order_hold_numpy(x2, xp2, yp2)
    # 488 µs ± 40.7 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
    # %timeit zero_order_hold(x2, xp2, yp2)
    # 494 µs ± 14.6 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
    # %timeit zero_order_hold(x2, xp2, yp2, assume_sorted=True)
    # 485 µs ± 15.3 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
