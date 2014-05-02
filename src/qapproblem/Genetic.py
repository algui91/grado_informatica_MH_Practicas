'''
Created on Apr 30, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''

from timeit import Timer

from qapproblem.Heuristic import Heuristic


class Genetic(Heuristic):
    
    def __init__(self, f_name, seed):
        super(Genetic, self).__init__(f_name, seed)
        
        def timewrapper():
            return self._find_solution()
        self.exec_time = Timer(timewrapper).timeit(number=1)
        
    def _find_solution(self):
        pass
