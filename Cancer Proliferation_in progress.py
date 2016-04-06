# -*- coding: utf-8 -*-
"""
Created on Wed Apr 06 11:26:29 2016

@author: Admin
"""

import numpy as np #numerical python
import matplotlib.pyplot as plt #Package used for plotting
from numba import jit, int64 # just in time compiler to speed up CA
import random

#### We build the world of our cancer cells####
def build_neighbor_pos_dictionary(n_row, n_col):
    """
    Create dictionary containing the list of all neighbors (value) for a central position (key)
    :param n_row:
    :param n_col:
    :return: dictionary where the key= central position, and the value=list of neighboring positions around that center
    """
    list_of_all_pos_in_ca = [(r, c) for r in np.arange(0, n_row) for c in np.arange(0, n_col)]

    dict_of_neighbors_pos_lists = {pos: build_neighbor_pos_list(pos, n_row, n_col) for pos in list_of_all_pos_in_ca}

    return dict_of_neighbors_pos_lists



def build_neighbor_pos_list(pos, n_row, n_col):
    """
    Valid positions are those that are within the confines of the domain (n_row, n_col)
    and not the same as the cell's current position.

    :param pos: cell's position; tuple
    :param n_row: maximum width of domain; integer
    :param n_col: maximum height of domain; integer
    :return: list of all valid positions around the cell
    """
    # Unpack the tuple containing the cell's position
    r, c = pos

    l = [(r+i, c+j)
         for i in [-1, 0, 1]
         for j in [-1, 0, 1]
         if 0 <= r + i < n_row
         if 0 <= c + j < n_col
         if not (j == 0 and i == 0)]

    return l
"""
#### METHODS TO SPEED UP EXECUTION ####
binomial = np.random.binomial
shuffle = np.random.shuffle
random_choice = random.choice
"""

@jit(int64(), nopython=True)  # NOTE: declaring the return type is not required
def divide_symmetrically_q():
    SYMMETRIC_DIVISION_PROB = 0.3 #3/10.0
    verdict = binomial(1, SYMMETRIC_DIVISION_PROB)

    return verdict


@jit(int64(), nopython=True)
def divide_q():
    DIVISION_PROB = 0.0416 #1 / 24.0
    verdict = binomial(1, DIVISION_PROB)

    return  verdict


@jit(int64(), nopython=True)
def die_q():
    DEATH_PROB = 0.01 #1 / 100.0
    verdict = binomial(1, DEATH_PROB)

    return verdict