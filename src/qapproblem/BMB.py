# -*- coding: utf-8 -*-

'''
Created on May 2, 2014

@author: hkr (elbauldelprogramador.com)

Licensed under GPLv3
'''
from timeit import Timer

from qapproblem.Heuristic import Heuristic
from qapproblem.LocalSearch import LocalSearch
from IN import SOL_AAL


class BMB(Heuristic):
    '''
    Basic multi boot Search
    '''

    n_random_sol = 25
    sol = []
    
    def __init__(self, f_name, seed):
        '''
        Constructor
        '''
        super(BMB, self).__init__(f_name, seed)

        def timewrapper():
            return self.find_solution()
        self.exec_time = Timer(timewrapper).timeit(number=1)
        
    def local_search(self, s):
        num_eval = 0
        max_evals = 10000
        improve_flag = True
        self._DLB = [0] * self._data.tam
        _DLB = self._DLB 
        self.S = s
        self.cost = self.C()
        tam = self._tam
        deltaC = self.deltaC
        swap = self.swap
        cost = self.cost
        S = self.S
        
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
                            cost += improvement
                            S = swap(i, j)
                            _DLB[i] = _DLB[j] = 0
                            improve_flag = True
                        j += 1
                    if not improve_flag:
                        _DLB[i] = 1
                i += 1
        return self.S, self.cost
        
    def find_solution(self):
        # Generate 25 random solutions
        
        append = self.sol.append
        get_random_sol = self.get_random_sol
        
        [append(get_random_sol()) for _ in xrange(self.n_random_sol-1)]
        
        self.sol.append(self.S)
        
        best_sol = self.sol[0]
        c_best = self.C(S=best_sol)
        
        self.sol = map(tuple, self.sol)
        self.sol = set(self.sol)
        
        LS = self.local_search
                
        for s in self.sol:
            sol, cost = LS(s)
            if cost < c_best:
                best_sol = sol
                c_best = cost
                
        self.S = best_sol
        self.cost = c_best
