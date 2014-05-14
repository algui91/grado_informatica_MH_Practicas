'''
Created on May 13, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''
import math
from timeit import Timer

from qapproblem.Genetic import GG_Base
from random import randint


class Elitist_GG_PMX(GG_Base):
    '''
    Implementation of a Elitist Genetic Algorithm with 
    PMX as crossover operator
    '''
    cross_prob = .7
    how_many_cross = int(math.ceil(cross_prob * (GG_Base.population_lenght / 2)))
    
    def __init__(self, f_name, seed):
        '''
        Constructor
        '''
        super(Elitist_GG_PMX, self).__init__(f_name, seed)
        
        def timewrapper():
            return self._find_solution()
        self.exec_time = Timer(timewrapper).timeit(number=1)
    
    def _find_solution(self):
        
        self.initPopulation()
        self.evaluate()
        
        while self.stop_crit >= 0:
            # swap current and old population
            self.old_population, self.current_population = self.current_population, self.old_population
            self.select()
            self.cross()
            self.mutate()
            self.reemplace()
            self.evaluate()
        
        self.S = self.best_guy[2]
        self.cost = self.best_current_cost
        
        print self.local_search(list(self.S))
        
    def cross(self):
        '''
        We need to cross `how_many_cross` individuals 
        with the PMX crossover operator
        '''
        
        for i in xrange(0, self.how_many_cross, 2):
            parent1 = self.current_population[i][2]
            parent2 = self.current_population[i + 1][2]
            
            child1, child2 = self.get_two_childs_PMX(parent1, parent2)
                
            self.current_population[i][2] = list(child1)
            self.current_population[i][0] = 1
            self.current_population[i + 1][2] = list(child2)
            self.current_population[i + 1][0] = 1
    
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