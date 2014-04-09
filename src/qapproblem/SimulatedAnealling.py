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
        self.T_0 = (self.mu * self.C()) / -log(self.prob)
        # Final temp
        self.T_f = 10**-3
        # Current Temp
        self.T = self.T_0
        # Number of repetitions
        self.nrep = 10000
        # Max number of neighbor
        self.max_neighbors = self._tam
        self.max_successes = .1 * self.max_neighbors
        
        self._find_solution()
        
    def _cooling_schedule(self):
        beta = (self.T_0 / self.T_f) / (self.nrep * self.T_0 * self.T_f)
        self.T = self.T / (1 + beta *self.T)
    
    
    def _find_solution(self):

        C_act = self.C()
        S_act = self.S
        best_C = C_act
        best_S = self.S
        #self.T = self.T_0
        
        while self.nrep:
            n_successes = 0
            neighbors_generated = 0
            while neighbors_generated < self.max_neighbors or n_successes < self.max_successes:
                # Generate a random neighbor
                neighbor = self.gen_neighbor()
                neighbors_generated += 1
                C_neighbor = self.C(neighbor)
                delta = C_neighbor - best_C
                if delta < 0:
                    n_successes += 1
                    S_act = neighbor
                    C_act = C_act + delta
                    best_S = neighbor
                    best_C = C_neighbor
                else:
                    accept_prob = exp(-delta/self.T)
                    n = random()
                    if n < accept_prob:
                        S_act = neighbor
                        C_act = C_act + delta
                        n_successes += 1
                    
                print 'Generate neighbor %s' % neighbor
                
            self.nrep -= 1
            self._cooling_schedule()

        return best_S, best_C
        