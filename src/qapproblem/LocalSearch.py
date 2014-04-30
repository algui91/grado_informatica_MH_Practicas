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
        num_eval = 0
        done = False

        # Falta el bucle externo hasta no mejora o num_eval <= 10000
        while num_eval < 10000 and not done:
            for i in xrange(self._tam):
                if self._DLB[i] == 0:
                    improve_flag = False
                    j = 0
                    while j < self._tam and not improve_flag and num_eval < 10000:
                        neighbor = self.swap(i, j)
                        improvement = self.deltaC(i, j)
                        num_eval += 1
                        if (improvement < 0):
                            self.cost += improvement
                            self.S = neighbor
                            self._DLB[i] = self._DLB[j] = 0
                            improve_flag = True
                        j += 1
                    if not improve_flag:
                        self._DLB[i] = 1
                print num_eval
            done = True
