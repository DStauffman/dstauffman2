# -*- coding: utf-8 -*-
r"""
Iteratively solves a cube for given sums by rows, columns and diagonals.
"""

#%% Imports
import numpy as np

#%% Functions - is_done
def is_done(A, h, v, d):
    # checks if the solution has been found
    temp = (np.sum(A, axis=1) == h) & (np.sum(A, axis=0) == v) & (np.sum(A[d1]) == d[0]) & (np.sum(A[d2]) == d[1])
    out  = np.all(temp)
    return out

#%% Functions - print_sums
def print_sums(A, h, v, d):
    r"""Prints the matrix along with the sums and errors."""
    # displays information about the current solution compared to the desired one
    print('A = ')
    print(A)
    print('Row sums    = {}, Want: {}, Error: {}'.format(np.sum(A, axis=1), h, h-np.sum(A, axis=1)))
    print('Column sums = {}, Want: {}, Error: {}'.format(np.sum(A, axis=0), v, v-np.sum(A, axis=0)))
    t = np.array([np.sum(A[d1]), np.sum(A[d2])])
    print('Diag sums   = {}, Want: {}, Error: {}'.format(t, d, d-t))

#%% Functions - enforce_minmax
def enforce_minmax(A):
    # enforces and minimum and maximum constraint
    out = np.maximum(np.minimum(A, 9), 1)
    return out

#%% Script
if __name__ == '__main__':
    #%% Given:
    A      = np.array([[0, 0, 0, 2], [0, 8, 0, 0], [9, 0, 0, 0], [0, 0, 7, 0]], dtype=float)
    horzs  = np.array([13, 31, 13, 25])
    verts  = np.array([33, 13, 14, 22])
    diags  = np.array([26, 15])
    A_soln = np.array([[8, 2, 1, 2], [9, 8, 5, 9], [9, 1, 1, 2], [7, 2, 7, 9]])

    #%% settings
    max_iters = 10
    round_dig = 4

    #%% alias useful values
    n    = A.shape[0]
    d1   = (np.arange(n), np.arange(n))
    d2   = (np.arange(n), np.arange(n-1, -1, -1))
    mask = A == 0

    #%% calculations
    # initialize working solution
    R = A.copy()
    # loop through iterative solver
    for it in range(max_iters):
        # horizontals
        delta_h = horzs - np.sum(R, axis=1)
        R += np.transpose(mask.T * np.round(delta_h / np.sum(mask, axis=1), round_dig))

        # verticals
        delta_v = verts - np.sum(R, axis=0)
        R += mask * np.round(delta_v / np.sum(mask, axis=0), round_dig)

        # diag one
        delta_d1 = diags[0] - np.sum(R[d1])
        temp = np.zeros((n, n))
        temp[d1] = np.round(delta_d1 / np.sum(mask[d1]), round_dig)
        R += mask * temp

        # diag two
        delta_d2 = diags[1] - np.sum(R[d2])
        temp = np.zeros((n, n))
        temp[d2] = np.round(delta_d2 / np.sum(mask[d2]), round_dig)
        R += mask * temp

        # enforce minimum and maximum constraints
        R = enforce_minmax(R)

        # check if done, and if so display results and exit solver loop
        if is_done(np.round(R), horzs, verts, diags):
            R = np.round(R).astype(int)
            print('Done on iteration: {}'.format(it+1))
            print_sums(R, horzs, verts, diags)
            break
        if it == max_iters - 1:
            # check if not done after reaching final iteration
            print('No exact solution found')
            R = np.round(R).astype(int)
        # display the current results
        print('Results after iteration: {}'.format(it+1))
        print_sums(R, horzs, verts, diags)