'''
Created on May 3, 2014

@author: hkr (elbauldelprogramador.com)

Licensed under GPLv3
'''
from operator import itemgetter
from random import random
from timeit import Timer

from qapproblem.Heuristic import Heuristic


class Grasp(Heuristic):
    '''
    Implementation of the GRASP algorithm
    '''

    n_random_sol = 25
    sol = []
    alpha = .3
    LC = []
    LRC = []
    LRC_u = []
    LRC_l = []
    LC_u = []
    LC_l = []
    
    def __init__(self, f_name, seed):
        '''
        Constructor
        '''
        super(Grasp, self).__init__(f_name, seed)

        def timewrapper():
            return self.find_solution()
        self.exec_time = Timer(timewrapper).timeit(number=1)
    
    def randomized_greedy(self):
        # Generate permutations of N
        # Stage 1, get best to assigments
        s = [self.LC[0][1], self.LC[1][1]]
        # Stage 2
        
    
    def potential(self, matrix):
        len_matrix = len(matrix)
        
        pot = []
        
        for i in xrange(len_matrix):
            for j in xrange(len_matrix):
                pot.append(matrix[i][j] + matrix[j][i])
        return pot 
        
    def get_permutations(self):
        x = self._tam        
        per = list()
        f = self._data.stream_matrix
        d = self._data.distance_matrix 
        
        for i in xrange(x):
            for k in xrange(x):
                for j in xrange(x):
                    for l in xrange(x):
                        if i != j and k != l:
                            cost = f[i][j] * d[k][l]
                            per.append([cost, (i, k), (j, l)])
                            
        per.sort(key=itemgetter(0))
        
        return per
        
    def find_solution(self):
        # Generate 25 random solutions
        
        # repeat until stop criteria
            # s <- Randomized Greedy (Best of LC)
            # s_ <- LS(s)
            # Update(s_, best_sollution)
            # return best_solution
            
        # Initialization phase
        self.LC = self.get_permutations()
        best_S = self.S
        best_cost = self.cost
        
        for _ in xrange(25):
            s_greedy = self.randomized_greedy()
            C_min, C_max = self.LC[0][0], self.LC[-1][0]
            self.LRC = self.LC[:C_min + self.alpha * (C_max - C_min)]
            rand = random.randint(0,len(self.LRC))
            s_grasp = [self.LRC[rand][1]]
            s_BL, cost_BL = self.local_search(s_greedy)
            if cost_BL < best_cost:
                best_cost = cost_BL
                best_S = s_BL
            
            
