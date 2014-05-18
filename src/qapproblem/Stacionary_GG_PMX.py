'''
Created on May 17, 2014

@author Alejandro Alcalde (elbauldelprogramador.com)

Licensed Under GPLv3
'''

from copy import deepcopy
import math
from random import randint
from timeit import Timer

from qapproblem.Genetic import GG_Base


class Stacionary_GG_PMX(GG_Base):
    '''
    Implementation of a estacionary Genetic Algorithm with 
    the PMX based crossover operator
    '''
    
    cross_prob = 1 # The parents always cross

    def __init__(self, f_name, seed):
        '''
        Constructor
        '''
        super(Stacionary_GG_PMX, self).__init__(f_name, seed)
        
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
            
        child1, child2 = self.get_two_childs_PMX(parent1, parent2)
                
            # Add the child to the population and mark it as need to evaluate
        if child1 != -1:
            new_gen[0][2] = list(child1)
            new_gen[0][0] = 1
            new_gen[1][2] = list(child2)
            new_gen[1][0] = 1

    def get_two_childs_PMX(self, p1, p2):
        '''
        Get two children based on the PMX operator
        '''
        cut1 = randint(0, self.n - 1)
        cut2 = randint(cut1, self.n - 1)
        cut2 += 1
        
        child1 = [0] * self.n
        child2 = list(child1)
        
        child1[cut1:cut2] = p2[cut1:cut2]
        child2[cut1:cut2] = p1[cut1:cut2]
        
        correspondences1 = []
        append_c_1 = correspondences1.append
        correspondences2 = []
        append_c_2 = correspondences2.append
        
        for i in p1[cut1:cut2]:
            append_c_1([p2[p1.index(i)],i])
        for i in p2[cut1:cut2]:
            append_c_2([p1[p2.index(i)],i])
            
        correspondences1.reverse()
        correspondences2.reverse()
        
        indexes_emtpy = set(xrange(self.n)) - set(xrange(cut1,cut2))
        
        already_in1 = child1[cut1:cut2]
        already_in2 = child2[cut1:cut2]
        
        for i in indexes_emtpy:
            if p1[i] in already_in1: 
                c = correspondences1.pop()
                while c[1] in already_in1:
                    c = correspondences1.pop()
                child1[i] = c[1]
            else:
                child1[i] = p1[i]
        
        for i in indexes_emtpy:
            if p2[i] in already_in2:
                c = correspondences2.pop()
                while c[1] in already_in2:
                    c = correspondences2.pop()
                child2[i] = c[1]
            else:
                child2[i] = p2[i] 
                
        return child1, child2  

    def reemplace(self, new_gen):
        '''
        The two current cromosomes generated replace two of the
        worst cromosomes in the previous population, if this two are
        better. 
        '''
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
