# -*- coding: utf-8 -*-

'''
Created on May 2, 2014

@author: hkr (elbauldelprogramador.com)

Licensed under GPLv3
'''
from timeit import Timer

from qapproblem.Heuristic import Heuristic


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
