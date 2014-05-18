'''
Created on May 13, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''
import math
from timeit import Timer

from qapproblem.Genetic import GG_Base


class Elitist_GG_pos(GG_Base):
    '''
    Implementation of a Elitist Genetic Algorithm with 
    position based crossover operator
    '''
    cross_prob = .7
    how_many_cross = int(math.ceil(cross_prob * (GG_Base.population_lenght / 2)))
    
    def __init__(self, f_name, seed):
        '''
        Constructor
        '''
        super(Elitist_GG_pos, self).__init__(f_name, seed)
        
        def timewrapper():
            return self._find_solution()
        self.exec_time = Timer(timewrapper).timeit(number=1)
    
    def _find_solution(self):
        
        
        population = self.population_lenght
        
        self.initPopulation()
        self.evaluate(population)
        
        while self.stop_crit >= 0:
            # swap current and old population
            self.old_population, self.current_population = self.current_population, self.old_population
            self.select(population)
            self.cross()
            self.mutate(population, self.how_many_mutate)
            self.reemplace()
            self.evaluate(population)
            
        self.S = self.best_guy[2]
        self.cost = self.best_current_cost
        
    def cross(self):
        '''
        We need to cross `how_many_cross` individuals 
        with position based crossing operator
        '''
        
        for i in xrange(0, self.how_many_cross, 2):
            parent1 = self.current_population[i][2]
            parent2 = self.current_population[i + 1][2]
            
            child1, child2 = self.get_two_childs(parent1, parent2)
                
            # Add the child to the population and mark it as need to evaluate
            if child1 != -1:
                self.current_population[i][2] = list(child1)
                self.current_population[i][0] = 1
                self.current_population[i + 1][2] = list(child2)
                self.current_population[i + 1][0] = 1
        