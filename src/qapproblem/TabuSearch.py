'''
Created on Apr 10, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''
import functools
from random import randint

from qapproblem.Heuristic import Heuristic


class TabuSearch(Heuristic):
    '''
    Implementation of TS for QAP
    '''

    def __init__(self, f_name, seed):
        '''
        Constructor
        '''
        super(TabuSearch, self).__init__(f_name, seed)
        self.neighbors_per_iter = 30
        self.reinit_counter     = 10
        self.n_iters            = 10000
        self.size_tabu_list     = self._tam/2
        self.tabu_list          = [[0 for _ in xrange(4)] for _ in xrange(self.size_tabu_list)]
        self.frequency          = [[0 for _ in xrange(self._tam)] for _ in xrange(self._tam)]
        self._find_solution()
        
    def _find_solution(self):
        best_S = self.S
        best_C = self.cost
        # Best solution for the current iteration 
        best_curr_iter_C = best_C
        best_curr_iter_S = best_S
        # Number of iterations without improving cost
        iter_no_imprv = 0
        # Movements counter for tabu list
        tabu_index = 0
        n_iter = 0
        
        while n_iter < self.n_iters:
            # Generate a group of neighbors
            neighbors = self.gen_group_of_neighbors(self.neighbors_per_iter)
            #neighbors.sort(key=functools.cmp_to_key(self._compare_costs))
            neig_picked = False
            
            neig_counter = 0
            while neig_counter < self.neighbors_per_iter and not neig_picked:
                tabu_index %= self.size_tabu_list
                r, s = neighbors[neig_counter][0], neighbors[neig_counter][1]
                tabu_element = (
                                r, # index swaped
                                s, # index swaped
                                neighbors[neig_counter][2][r],
                                neighbors[neig_counter][2][s]
                                )
                if ((not self._is_tabu(tabu_element)) or self._aspiration_criterion(best_S, r, s)):
                    neig_picked = True
                    self.tabu_list[tabu_index] = tabu_element
                    tabu_index += 1
                    self.S = self.gen_neighbor()[2]
                    self.cost = self.C()
                    n_iter += 1
                    self.frequency[r][self.S[s]] += 1
                    self.frequency[s][self.S[r]] += 1
                    if (self.cost < best_C):
                        n_iter += 1
                        best_S = self.S
                        best_C = self.cost
                neig_counter += 1
            
            if best_curr_iter_C == best_C:
                iter_no_imprv += 1
            elif best_C < best_curr_iter_C:
                best_curr_iter_C = best_C
                iter_no_imprv = 0
            if iter_no_imprv == self.reinit_counter:
                iter_no_imprv = 0
                new_tam_tl = randint(0,1)
                if new_tam_tl == 0:
                    self.size_tabu_list += self.size_tabu_list/2
                else:
                    self.size_tabu_list -= self.size_tabu_list/2
                self.tabu_list = [[0 for _ in xrange(4)] for _ in xrange(self.size_tabu_list)]
                
                i = randint(0,3)
                
                if i == 1:
                    r, s, self.S = self.gen_neighbor()
                    self.cost += self.deltaC(r, s)
                elif i == 0:
                    self.S = best_S
                    self.cost = best_C
                elif i == 2 or i == 3:
                    pass
            
        return best_S, best_C
     
    def _aspiration_criterion(self, best, r, s):
        return self.deltaC(r, s, best) < 0
    
    def _is_tabu(self, neig):
        for i in xrange(len(self.tabu_list)):
            if ( (neig[0] == self.tabu_list[i][0] and neig[2] == self.tabu_list[i][2]) or
                 (neig[0] == self.tabu_list[i][1] and neig[2] == self.tabu_list[i][3]) or
                 (neig[1] == self.tabu_list[i][1] and neig[3] == self.tabu_list[i][3]) or
                 (neig[1] == self.tabu_list[i][0] and neig[3] == self.tabu_list[i][2])):
                return True
        return False
                
    def _compare_costs(self, a, b):
        r_a, s_a = a[0], a[1]
        r_b, s_b = b[0], b[1]
        
        delta_a = self.deltaC(r_a, s_a)
        delta_b =self.deltaC(r_b, s_b)
        
        if ( delta_a < delta_b):
            return -1
        elif (delta_a == delta_b):
            return 0
        else:
            return 1