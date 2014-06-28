'''
Created on June 27, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''
from timeit import Timer

from qapproblem.MA_10_1_PMX import MA_10_1_PMX


class MA_10_01_PMX(MA_10_1_PMX):
    '''
    A memetic genetic algorithm with local search. Every 10 generations
    local search is applied to the population with probability 0.1.
     
    PMX as crossover operator
    '''
    
    def __init__(self, f_name, seed):
        '''
        Constructor
        '''
        super(MA_10_01_PMX, self).__init__(f_name, seed)
        
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
                for i in xrange(self.population_lenght * .1):
                    (
                        self.current_population[i][2],
                        self.current_population[i][1],
                        num_evals 
                    ) = self.local_search(self.current_population[i][2], 400)
                    self.stop_crit -= num_evals
                generation_number = 0
        
        self.S = self.best_guy[2]
        self.cost = self.best_current_cost  
