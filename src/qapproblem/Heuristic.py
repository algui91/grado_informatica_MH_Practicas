# -*- coding: utf-8 -*-

'''
Created on Apr 1, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''

from qapproblem.Data import Data

class Heuristic(object):
    '''
    Common operations for all implemented Heuristics
    '''
    
    # Vector with the permutation for the solution
    S = []
    cost = 0
    
    def __init__(self, file_name):
        self._data = Data(file_name)
        self._tam = self._data.tam
        
    def C(self, S=None):
        '''
        Cost of the solution with permutation S
        '''
        cost = 0
        
        for i in xrange(self._tam):
            for j in xrange(self._tam):
                cost += self._data.stream_matrix[i][j] * self._data.distance_matrix[self.S[i]][self.S[j]]
        
        self.cost = cost
        
        