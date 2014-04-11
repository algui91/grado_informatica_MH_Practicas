'''
Created on Apr 2, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''
from timeit import Timer

from qapproblem.Heuristic import Heuristic


class LocalSearch(Heuristic):
    '''
    Local Search with Don't look bits
    '''

    def __init__(self, f_name, seed):
        '''
        Constructor
        '''
        super(LocalSearch, self).__init__(f_name, seed)
        self._DLB = [0] * self._data.tam
        
        def timewrapper():
            return self._find_solution()
        self.exec_time =  Timer(timewrapper).timeit(number=1)
        
    def _find_solution(self):
        for i in xrange(self._tam):
            if self._DLB[i] == 0:
                improve_flag = False
                for j in xrange(self._tam):
                    neighbor = self.swap(i, j)
                    improvement = self.deltaC(i, j)
                    if (improvement < 0):
                        self.cost += improvement
                        self.S = neighbor
                        self._DLB[i] = self._DLB[j] = 0
                        improve_flag = True
                if not improve_flag:
                    self._DLB[i] = 1