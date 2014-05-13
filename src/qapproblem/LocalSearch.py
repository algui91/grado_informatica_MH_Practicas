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

    def __init__(self, f_name, seed, S, Cost):
        '''
        Constructor
        '''
        super(LocalSearch, self).__init__(f_name, seed)
        self._DLB = [0] * self._data.tam

        self.S = S
        self.cost = Cost
        def timewrapper():
            return self.find_solution()
        self.exec_time =  Timer(timewrapper).timeit(number=1)

    def find_solution(self):
        num_eval = 0
        max_evals = 10000
        improve_flag = True
        _DLB = self._DLB 
        tam = self._tam
        deltaC = self.deltaC
        swap = self.swap
        cost = self.cost
        
        while num_eval < max_evals and improve_flag:
            improve_flag = False
            i = 0
            while i < tam and not improve_flag:
                if _DLB[i] == 0:
                    j = 0
                    while j < tam and not improve_flag:
                        improvement = deltaC(i, j)
                        num_eval += 1
                        if (improvement < 0):
                            self.cost += improvement
                            self.S = swap(i, j)
                            _DLB[i] = _DLB[j] = 0
                            improve_flag = True
                        j += 1
                    if not improve_flag:
                        _DLB[i] = 1
                i += 1