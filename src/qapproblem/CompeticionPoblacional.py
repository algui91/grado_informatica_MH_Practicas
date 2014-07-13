'''
Created on June 27, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''
import heapq
from operator import itemgetter
from timeit import Timer

from qapproblem.MA_10_1_PMX import MA_10_1_PMX


class CompeticionPoblacional(MA_10_1_PMX):
    '''
    A memetic genetic algorithm with local search. Every 10 generations
    local search is applied to the population with probability 0.1.
     
    PMX as crossover operator
    '''
    
    population_lenght = 50
    old_population = [0] * population_lenght
    stop_crit = 100000
    
    
    def __init__(self, f_name, seed):
        '''
        Constructor
        '''
        super(CompeticionPoblacional, self).__init__(f_name, seed)
        
             
        def timewrapper():
            return self._find_solution()
        self.exec_time = Timer(timewrapper).timeit(number=1)
    
    def _find_solution(self):
        
        population = self.population_lenght
        
        self.initPopulation()
        self.evaluate(population)
        
        generation_number = 0
        
        while self.stop_crit >= 0:
            
            # swap current and old population
            self.old_population, self.current_population = self.current_population, self.old_population
            self.select(population)
            self.cross()
            self.mutate(population, self.how_many_mutate)
            self.reemplace()
            self.evaluate(population)
            
            generation_number += 1
            
            if generation_number == 10:
                for i in xrange(int(self.population_lenght * .1)):
                    (
                        self.current_population[i][2],
                        self.current_population[i][1],
                        num_evals 
                    ) = self.local_search(self.current_population[i][2], 400)
                    self.stop_crit -= num_evals
                generation_number = 0
        
        self.S = self.best_guy[2]
        self.cost = self.best_current_cost  
        
    def cross(self):
        '''
        We need to cross `how_many_cross` individuals 
        with the SPX operator (Swap Path Crossover)
        '''
        
        for i in xrange(0, self.how_many_cross, 2):
            parent1 = self.current_population[i][2]
            parent2 = self.current_population[i + 1][2]
            
            child1, child2 = self.get_two_childs_SPX(parent1, parent2)
                
            self.current_population[i][2] = list(child1)
            self.current_population[i][0] = 1
            self.current_population[i + 1][2] = list(child2)
            self.current_population[i + 1][0] = 1
            
    def get_two_childs_SPX(self, p1, p2):
        '''
        Get two children based on the SPX operator (Swap Path Crossover)
        '''
        #cut1 = randint(0, self.n - 1)
        
        childs = []
        append = childs.append
        C = self.C
        
        child1 = list(p1)
        
        for i in xrange(self.n):
            if p1[i] != p2[i]:
                index1 = p1.index(p2[i])
                child1[i], child1[index1] = child1[index1], child1[i]
                [append([C(child1), list(child1)])]
        
        # Remove repeated results
        for c in childs:
            c[1] = tuple(c[1])
        childs = map(tuple, childs)
        childs = set(childs)
        
        best_guys = heapq.nsmallest(2, childs, key=itemgetter(0))
        
        if best_guys == []:
            return p1, p2
        return best_guys[0][1], best_guys[1][1]
        