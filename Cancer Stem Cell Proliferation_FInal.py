# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 16:40:52 2016

@author: Madhav
"""
"""GUIDE TO THE MODEL PROJECT
A cell, either cancer stem cell (CSC) or non-stem cancer cell (CC), occupies a single 
grid point on a two-dimensional square lattice. CSCs have unlimited proliferation 
potential and at each division they produce either another CSC (symmetric division) 
or a CC (asymmetric division). CCs are eroding their proliferation potential at each 
division and die when its value reaches 0. Moreover, at each proliferation attempt, CCs 
may undergo spontaneous death and then be removed from the system."""

"""Certain probabilistic assumptions
Probability of proliferation = 1/24
Probability of death = 1/100
Initial Proliferation Capacity = 10
Probability of symmetric Division = 3/10"""

import numpy as np #numerical python
import matplotlib.pyplot as plt #Package used for plotting
import random

#### METHODS TO BUILD THE WORLD OF OUR PROLIFERATING CANCER STEM CELLS ####
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

    :param pos: cell's position; tuple
    :param n_row: maximum width of domain; integer
    :param n_col: maximum height of domain; integer
    
    
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

binomial = np.random.binomial
shuffle = np.random.shuffle
random_choice = random.choice


def divide_symmetrically_q():
    SYMMETRIC_DIVISION_PROB = 0.3 #3/10.0
    verdict = binomial(1, SYMMETRIC_DIVISION_PROB)

    return verdict



def divide_q():
    DIVISION_PROB = 0.0416 #1 / 24.0
    verdict = binomial(1, DIVISION_PROB)

    return  verdict



def die_q():
    DEATH_PROB = 0.01 #1 / 100.0
    verdict = binomial(1, DEATH_PROB)

    return verdict

#### CREATE CELL CLASSES ####
class CancerCell(object):

    def __init__(self, pos, dictionary_of_neighbor_pos_lists):
        """
        Initialize Cancer Cell
        :param pos: position of cancer cell; tuple
        :param dictionary_of_neighbor_pos_lists: used to tell the cell the positions of its neighbors
        :return:
        """

        self.pos = pos
        self.divisions_remaining = 10
        self.neighbor_pos_list = dictionary_of_neighbor_pos_lists[self.pos]
        self.PLOT_ID = 1

    def locate_empty_neighbor_position(self, agent_dictionary):
        """
        Search for empty positions in Moore neighborhood. If there is more thant one free position,
        randomly select one and return it

        :param agent_dictionary: dictionary of agents, key=position, value = cell; dict
        :return: Randomly selected empty position, or None if no empty positions
        """

        empty_neighbor_pos_list = [pos for pos in self.neighbor_pos_list if pos not in agent_dictionary]
        if empty_neighbor_pos_list:
            empty_pos = random_choice(empty_neighbor_pos_list)
            return empty_pos

        else:
            return None

    def act(self, agent_dictionary, dictionary_of_neighbor_pos_lists):
        """
        Cell carries out its actions, which are division and death. Cell will divide if it is lucky and
        there is an empty position in its neighborhood. Cell dies either spontaneously or if it exceeds its
        maximum number of divisions.

        :param agent_dictionary: dictionary of agents, key=position, value = cell; dict
        :return: None
        """

        #### CELL TRIES TO DIVIDE ####
        divide = divide_q()
        if divide == 1:
            empty_pos = self.locate_empty_neighbor_position(agent_dictionary)
            if empty_pos is not None:

                #### CREATE NEW DAUGHTER CELL AND IT TO THE CELL DICTIONARY ####
                daughter_cell = CancerCell(empty_pos, dictionary_of_neighbor_pos_lists)
                agent_dictionary[empty_pos] = daughter_cell

                self.divisions_remaining -= 1

        #### DETERMINE IF CELL WILL DIE ####
        spontaneous_death = die_q()
        if self.divisions_remaining <= 0 or spontaneous_death == 1:
            del agent_dictionary[self.pos]

class CancerStemCell(CancerCell):

    def __init__(self, pos, dictionary_of_neighbor_pos_lists):
        """
        Inherits explicitly from CancerCell Class.

        Difference between cancer stem cells and cancer cells is that the former are immortal, have infinite replicative
        potential, and can divide either symmetrically or asymmetrically

        :param pos: cell's position; tuple
        :return: CancerStemCell object
        """
        super(CancerStemCell, self).__init__(pos, dictionary_of_neighbor_pos_lists)
        self.PLOT_ID = 2

    def act(self, agent_dictionary, dictionary_of_neighbor_pos_lists):
        """
        Cancer stem cell carries out its actions, which is to divide.

        :param agent_dictionary: dictionary of agents, key=position, value = cell; dict
        :return: None
        """

        divide = divide_q()
        if divide == 1:

            empty_pos = self.locate_empty_neighbor_position(agent_dictionary)
            if empty_pos is not None:

                symmetric_division = divide_symmetrically_q()
                if symmetric_division == 1:
                    daughter_cell = CancerStemCell(empty_pos, dictionary_of_neighbor_pos_lists)

                else:
                    daughter_cell = CancerCell(empty_pos, dictionary_of_neighbor_pos_lists)

                agent_dictionary[empty_pos] = daughter_cell


"""Time to Proliferate"""
if __name__ == "__main__":

    import time
    start = time.time()

    N_ROW = 100
    N_COL = 100
    MAX_REPS  = 500
    DICTIONARY_OF_NEIGHBOR_POS_LISTS = build_neighbor_pos_dictionary(N_ROW, N_COL)

    center_r = int(round(N_ROW/2.0))
    center_c = int(round(N_COL/2.0))
    center_pos = (center_r, center_c)

    initial_cancer_stem_cell = CancerStemCell(center_pos, DICTIONARY_OF_NEIGHBOR_POS_LISTS)
    cell_dictionary = {center_pos:initial_cancer_stem_cell}

    for rep in range(MAX_REPS):
        
        cell_list = cell_dictionary.values()
        
        
        shuffle(cell_list)

        for cell in cell_list:
            cell.act(cell_dictionary, DICTIONARY_OF_NEIGHBOR_POS_LISTS)



    visualization_matrix = np.zeros((N_ROW, N_COL))
    for cell in cell_dictionary.values():
        visualization_matrix[cell.pos] = cell.PLOT_ID
        plt.pause(0.5)
        plt.title("Stem Cell Proliferation")
        plt.imshow(visualization_matrix, interpolation='none', cmap='seismic', vmin=0, vmax=2)
    
    plt.savefig("./CSC_CA.png", dpi=300)

    end = time.time()
    total = end-start
    print("total time", total)
    
"""THAT'S ALL FOLKS"""