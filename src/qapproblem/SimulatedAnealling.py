'''
Created on Apr 4, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''
from math import log
from math import exp
from random import random

from qapproblem.Heuristic import Heuristic


class SimulatedAnealling(Heuristic):
    '''
    Implementation of Simulated Anealling algorithm for QAP
    '''

    def __init__(self, file_name, seed):
        '''
        Constructor
        '''
        super(SimulatedAnealling, self).__init__(file_name, seed)
        
        # Probability of accept solution 1/mu
        self.mu = self.prob = .3
        # Initial temp
        self.T_0 = (self.mu * self.cost) / -log(self.prob)
        # Final temp
        self.T_f = 10**-3
        # Current Temp
        self.T = self.T_0
        # Number of repetitions
        self.n_iter = 10000.0 / self._tam
        # Max number of neighbor
        self.max_neighbors = self._tam
        
        self.max_successes = .1 * self.max_neighbors
        
        
        self.n_eval = 0
        self.S, self.cost = self._find_solution()
        
    def _cooling_schedule(self):
        beta = (self.T_0 / self.T_f) / (self.n_iter * self.T_0 * self.T_f)
        self.T = self.T / (1 + beta * self.T)
    
    def _find_solution(self):

        best_C = self.cost
        best_S = self.S
        
        while self.n_eval < 10000:
            n_successes = 0
            neighbors_generated = 0
            while neighbors_generated < self.max_neighbors or n_successes < self.max_successes:
                # Generate a random neighbor
                r, s, neighbor = self.gen_neighbor()
                neighbors_generated += 1
                delta_neighbor = self.deltaC(r, s)
                self.n_eval += 1
                
                if delta_neighbor < 0 or (random() <= exp(-delta_neighbor/self.T)):
                    self.S = neighbor
                    self.cost += delta_neighbor
                    n_successes += 1
                    if (self.cost < best_C):
                        best_C = self.cost
                        best_S = self.S
                
            self._cooling_schedule()
            self.n_iter -= 1

        return best_S, best_C 