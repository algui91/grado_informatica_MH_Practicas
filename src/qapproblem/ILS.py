'''
Created on May 6, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''
import math
import random
from timeit import Timer

from qapproblem.Heuristic import Heuristic


class ILS(Heuristic):
    '''
    Implementation of the ILS algorithm
    
    ILS:
        S_0 = generate_init_solution
        S = LS(S_0)
        repeat
            s' <- modify(S, history) // Mutation
            s'' <- LS(s')
            s <- accept criteria(S,S'',history)
            update(S,best_S)
        until(stop criteria)
    '''


    def __init__(self, f_name, seed):
        '''
        Constructor
        '''
        super(ILS, self).__init__(f_name, seed)

        self.t = int(math.ceil(self._tam / 4.0))

        def timewrapper():
            return self.find_solution()
        self.exec_time = Timer(timewrapper).timeit(number=1)
    
    def mutate(self,s):
        '''
        Perform a mutation based on random sublist fixed size t t = (n/4)
        '''
        n = self._tam
        x = list(s)
        
        i = random.randint(0,n-1)
        items_to_change = ( i + self.t ) - i + 1
        upper = i + self.t
        current = i
        
        for _ in xrange(items_to_change):
            new_index = random.randint(i,upper) % n
            x[current], x[new_index] = x[new_index], x[current]
            current = (current+1) % n
        
        return x
    
        '''
    Implementation of the ILS algorithm
    
    ILS:
        S_0 = generate_init_solution
        S = LS(S_0)
        repeat
            s' <- modify(S, history) // Mutation
            s'' <- LS(s')
            s <- accept criteria(S,S'',history)
            update(S,best_S)
        until(stop criteria)
    '''
    
    def find_solution(self):

        best_S = self.S
        best_cost = self.cost

        
        S_0 = self.S
        S, S_cost = self.local_search(S_0)
        
        if S_cost < best_cost:
            best_cost = S_cost
            best_S = S
        else:
            S = best_S
            S_cost = best_cost
            
        for _ in xrange(24):
            S_p = self.mutate(S) 
            S_pp, S_pp_cost = self.local_search(S_p)

            if S_pp_cost < best_cost:
                S = S_pp
                S_cost = S_pp_cost 
                best_cost = S_cost
                best_S = S
        
        self.S = best_S
        self.cost = best_cost
        
