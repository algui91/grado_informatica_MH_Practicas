# -*- coding: utf-8 -*-

'''
Created on Apr 1, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''

import random
import numpy as np

from operator import itemgetter

class Heuristic(object):
    '''
    Common operations for all implemented Heuristics
    '''
    
    # Vector with the permutation for the solution
    S = []
    cost = 0
    seed = 0
    exec_time = 0
    
    def __init__(self, f_name, seed):
        # Initialize our seed
        random.seed(seed)
        self.seed = seed
        self._data = f_name
        self._tam = self._data.tam
        self._gen_random_sol()
        
    def _gen_random_sol(self):
        while len(self.S) < self._tam:
            r = random.randint(0,self._tam-1)
            if r not in self.S:
                self.S.append(r)
                
        self.cost = self.C()
                        
    def C(self, S=None):
        '''
        Cost of the solution with permutation S
        Hay que contar el número de búsquedas, limitado a 10000
        '''
        cost = 0

        if S is not None:
            s = S 
        else:
            s = self.S
        
        for i in xrange(self._tam):
            for j in xrange(self._tam):
                cost += self._data.stream_matrix[i][j] * self._data.distance_matrix[s[i]][s[j]]
           
        return cost
    
    def swap(self,i,j):
        s = list(self.S)
        s[i], s[j] = s[j], s[i]
        
        return s

    def deltaC(self, r, s, sol=None):
        delta = 0
        sol = self.S if sol is None else self.S
        sol_r, sol_s = sol[r], sol[s]
        
        stream_matrix = self._data.stream_matrix
        distance_matrix = self._data.distance_matrix
        
        indexes = set(xrange(self._tam)) - set([r, s])

        for k in indexes:
            sol_k = sol[k]
            delta += \
                (stream_matrix[r][k] - stream_matrix[s][k]) \
                * (distance_matrix[sol_s][sol_k] - distance_matrix[sol_r][sol_k]) \
                + \
                (stream_matrix[k][r] - stream_matrix[k][s]) \
                * (distance_matrix[sol_k][sol_s] - distance_matrix[sol_k][sol_r])
        return delta

    def gen_group_of_neighbors(self, number): 
        
        r, s = np.random.randint(0, self._tam, (2, number))
        p = zip(r, s)
        neig = [[p, q, self.deltaC(p, q)] for p, q in zip(r, s)]
        
        neig.sort(key=itemgetter(2))
        
        return neig

    def gen_neighbor(self):
        '''
        Performs a swap between two elements in S to produce a neighbor solution
        '''
        r = random.randint(0,self._tam-1)
        s = random.randint(0,self._tam-1)
        
        return r, s, self.swap(r, s)
        
