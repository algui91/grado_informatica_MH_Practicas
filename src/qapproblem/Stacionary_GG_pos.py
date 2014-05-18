'''
Created on May 17, 2014

@author Alejandro Alcalde (elbauldelprogramador.com)

Licensed Under GPLv3
'''

from copy import deepcopy
import math
from timeit import Timer

from qapproblem.Genetic import GG_Base


class Stacionary_GG_pos(GG_Base):
    '''
    Implementation of a estacionary Genetic Algorithm with 
    the position based crossover operator
    '''
    
    cross_prob = 1 # The parents always cross

    def __init__(self, f_name, seed):
        '''
        Constructor
        '''
        super(Stacionary_GG_pos, self).__init__(f_name, seed)
        
        self.num_genes = 2 * self.n 
        # How many will mutate (genes per individual  * num individual * prob mutation) 
        self.how_many_mutate = int(math.ceil(self.num_genes * self.mutation_prob))
        
        def timewrapper():
            return self._find_solution()
        self.exec_time = Timer(timewrapper).timeit(number=1)
         
    def _find_solution(self):
        
        self.initPopulation()
        self.evaluate(self.population_lenght)
        
        how_many = self.how_many_mutate
        
        while self.stop_crit >= 0:
            self.old_population = self.current_population
            new_gen = self.select(2, True) # Make two tournaments to pick two parents
            self.cross(new_gen)
            self.mutate(2, how_many, new_gen)
            self.reemplace(new_gen)
            self.evaluate(2, new_gen)
            
        self.S = self.best_guy[2]
        self.cost = self.best_current_cost
        
    def cross(self, new_gen):
        '''
        We need to cross `how_many_cross` individuals 
        with position based crossing operator
        '''

        parent1 = new_gen[0][2]
        parent2 = new_gen[1][2]
            
        child1, child2 = self.get_two_childs(parent1, parent2)
                
            # Add the child to the population and mark it as need to evaluate
        if child1 != -1:
            new_gen[0][2] = list(child1)
            new_gen[0][0] = 1
            new_gen[1][2] = list(child2)
            new_gen[1][0] = 1

    def reemplace(self, new_gen):
        '''
        The two current cromosomes generated replace two of the
        worst cromosomes in the previous population, if this two are
        better. 
        '''
        if self.current_population[self.index_worst_guy1][1] > new_gen[0][1]:
            self.current_population[self.index_worst_guy1] = deepcopy(new_gen[0])
        if self.current_population[self.index_worst_guy2][1] > new_gen[1][1]:
            self.current_population[self.index_worst_guy2] = deepcopy(new_gen[1])
        if self.current_population[self.index_worst_guy1][1] > new_gen[1][1]:
            self.current_population[self.index_worst_guy1] = deepcopy(new_gen[1])
        if self.current_population[self.index_worst_guy2][1] > new_gen[0][1]:
            self.current_population[self.index_worst_guy2] = deepcopy(new_gen[0])
