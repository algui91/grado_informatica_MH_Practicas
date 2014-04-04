# -*- coding: utf-8 -*-

'''
Created on Apr 1, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''

import random

class Heuristic(object):
    '''
    Common operations for all implemented Heuristics
    '''
    
    # Vector with the permutation for the solution
    S = []
    cost = 0
    seed = 0
    
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
                
        ## TODO: quitar
        self.C()
        #print 'Initial Random S =  %s, C(S) = %d, seed = %s\n\n\n' % (self.S, self.cost, self.seed)
                
    def C(self, S=None):
        '''
        Cost of the solution with permutation S
        Hay que contar el número de búsquedas, limitado a 10000
        '''
        cost = 0
        
        for i in xrange(self._tam):
            for j in xrange(self._tam):
                cost += self._data.stream_matrix[i][j] * self._data.distance_matrix[self.S[i]][self.S[j]]
        
        self.cost = cost    
        return cost
    
    def swap(self,i,j):
        s = list(self.S)
        s[i], s[j] = s[j], s[i]
        
        return s
    
    def deltaC(self, r, s):
        '''
        Difference between C with values i and j swapped
        '''
        delta = 0
        for k in xrange(self._tam):
            if k != r and k != s:
                delta += (self._data.stream_matrix[r][k] \
                    * (self._data.distance_matrix[self.S[s]][self.S[k]] - self._data.distance_matrix[self.S[r]][self.S[k]]) + \
                    self._data.stream_matrix[s][k] \
                    * (self._data.distance_matrix[self.S[r]][self.S[k]] - self._data.distance_matrix[self.S[s]][self.S[k]]) + \
                    self._data.stream_matrix[k][r] \
                    * (self._data.distance_matrix[self.S[k]][self.S[s]] - self._data.distance_matrix[self.S[k]][self.S[r]]) + \
                    self._data.stream_matrix[k][s] \
                    * (self._data.distance_matrix[self.S[k]][self.S[r]] - self._data.distance_matrix[self.S[k]][self.S[s]]))
        return delta

    def gen_neighbor(self):
        '''
        Performs a swap between two elements in S to produce a neighbor solution
        '''
        pass