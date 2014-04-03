# -*- coding: utf-8 -*-

'''
Created on Apr 1, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''
from qapproblem.Heuristic import Heuristic


class Greedy(Heuristic):
    '''
    Class for encapsulate the greedy algorithm
    '''

    _delta_distance = []
    _delta_stream = []
    
    def __init__(self, f_name):
        '''
        Constructor
        '''
        super(Greedy, self).__init__(f_name)
        
        self._delta_distance = self._delta(self._data.distance_matrix)
        self._delta_stream = self._delta(self._data.stream_matrix)
        
        self._find_solution()
        
    def _delta(self, matrix):
        '''
        Calcule the sum of rows in a matrix (Delta)
        
        @return: A list with the sum of the rows
        '''
        return [sum(i) for i in matrix]
    
    def _find_solution(self):
        
        copy_of_streams = self._delta_stream[:]
        copy_of_distances = self._delta_distance[:]
        self.S = list(None for _ in xrange(self._tam))
        
        for _ in xrange(self._tam):
            new_unit = max(copy_of_streams)
            new_location = min(x for x in copy_of_distances if x is not None)
            
            index_stream = copy_of_streams.index(new_unit)
            index_distance = copy_of_distances.index(new_location)
            
            self.S[index_stream] = index_distance

            copy_of_streams[copy_of_streams.index(new_unit)] =  None
            copy_of_distances[copy_of_distances.index(new_location)] = None
            
        self.C()