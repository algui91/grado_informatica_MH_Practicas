# -*- coding: utf-8 -*-

'''
Created on Apr 1, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''

import random
import numpy as np

from operator import itemgetter

class Heuristic(object):
    '''
    Common operations for all implemented Heuristics
    '''
    
    # Vector with the permutation for the solution
    S = []
    cost = 0
    seed = 0
    exec_time = 0
    
    def __init__(self, f_name, seed):
        # Initialize our seed
        random.seed(seed)
        self.seed = seed
        self._data = f_name
        self._tam = self._data.tam
        self.gen_random_sol()
        
    def gen_random_sol(self):
        while len(self.S) < self._tam:
            r = random.randint(0, self._tam - 1)
            if r not in self.S:
                self.S.append(r)
                
        self.cost = self.C()
        
    def get_random_sol(self):
        
        s = []
        tam = self._tam
        tam_gen = tam-1
        randint = random.randint
        append = s.append
        
        while len(s) < tam:
            r = randint(0, tam_gen)
            if r not in s:
                append(r)
        return s
                        
    def C(self, S=None):
        '''
        Cost of the solution with permutation S
        Hay que contar el número de búsquedas, limitado a 10000
        '''
        cost = 0

        if S is not None:
            s = S 
        else:
            s = self.S
        
        # self.S = map(int,"2 19 6 17 8 11 18 3 9 10 0 5 14 7 1 4 13 15 12 16".split())
        
        for i in xrange(self._tam):
            for j in xrange(self._tam):
                cost += self._data.stream_matrix[i][j] * self._data.distance_matrix[s[i]][s[j]]

        return cost
    
    def swap(self, i, j):
        s = list(self.S)
        s[i], s[j] = s[j], s[i]
        
        return s

    def deltaC(self, r, s, sol=None):
        delta = 0
        if sol == None:
            sol = self.S
        sol_r, sol_s = sol[r], sol[s]
        
        f = self._data.stream_matrix
        d = self._data.distance_matrix

        indexes = set(xrange(self._tam)) - set([r, s])

        for k in indexes:
            sol_k = sol[k]
            f_rk = f[r][k]
            f_sk = f[s][k]
            f_kr = f[k][r]
            f_ks = f[k][s]
            d_sol_sk = d[sol_s][sol_k]
            d_sol_rk = d[sol_r][sol_k]
            d_sol_ks = d[sol_k][sol_s]
            d_sol_kr = d[sol_k][sol_r]
            
            
            delta += f[r][k] * (d[sol_s][sol_k] - d[sol_r][sol_k]) + \
    				 f[s][k] * (d[sol_r][sol_k] - d[sol_s][sol_k]) + \
    				 f[k][r] * (d[sol_k][sol_s] - d[sol_k][sol_r]) + \
    				 f[k][s] * (d[sol_k][sol_r] - d[sol_k][sol_s])
        return delta

    def gen_group_of_neighbors(self, number): 
        
        r, s = np.random.randint(0, self._tam, (2, number))
        p = zip(r, s)
        neig = [[p, q, self.deltaC(p, q)] for p, q in zip(r, s)]
        
        neig.sort(key=itemgetter(2))
        
        return neig

    def gen_neighbor(self):
        '''
        Performs a swap between two elements in S to produce a neighbor solution
        '''
        r = random.randint(0, self._tam - 1)
        s = random.randint(0, self._tam - 1)
        
        return r, s, self.swap(r, s)
    
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
        #print 'Veces llamada ' , num_eval
        
        return self.S, self.cost
        
