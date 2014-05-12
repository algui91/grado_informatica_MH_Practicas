'''
Created on Apr 30, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''

import math
from operator import itemgetter
import random
from timeit import Timer

from qapproblem.Heuristic import Heuristic


class AGG(Heuristic):
    '''
    Elitist Genetic Algorithm with position based crossing operator
    '''
    population_lenght = 50
    cross_prob = .7  # 1 for AGO
    mutation_prob = .01
    stop_crit = 20000
    how_many_cross = int(math.ceil(cross_prob * (population_lenght / 2)))
    
    current_population = []
    old_population = [0] * population_lenght
    best_current_cost = 10**10
#    worst_current_cost = 0
    best_guy = []
#    worst_guy = []
    index_best_guy = 0
#    index_worst_guy = 0
    
    def __init__(self, f_name, seed):
        super(AGG, self).__init__(f_name, seed)
        
        self.n = self._tam
        self.num_genes = self.population_lenght * self.n 
        # How many will mutate (genes per individual  * num individual * prob mutation) 
        self.how_many_mutate = int(math.ceil(self.num_genes * self.mutation_prob))
        
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
        
    def initPopulation(self):
        '''
        Randomly generate the initial population
        '''
        append = self.current_population.append
        get_random_sol = self.get_random_sol
        
        # First element is a list  representing [not_evaluated, cost, S]
        [append([1, 0, get_random_sol()]) for _ in xrange(self.population_lenght)]
    
    def evaluate(self):
        '''
        Evaluate the population
        '''
        population = self.current_population
        C = self.C
        stop_criteria = self.stop_crit
        
        for i in xrange(self.population_lenght):
            p = population[i]
            if p[0]: # need to re-evaluate
                p[1] = C(p[2])
                self.stop_crit -= 1
                p[0] = 0 # mark it as evaluated
                stop_criteria -= 1
            if p[1] < self.best_current_cost:
                self.best_guy = p
                self.best_current_cost = p[1]
                self.index_best_guy = i
    
    def select(self):
        '''
        Select two individuals by tournament
        '''

        for i in xrange(self.population_lenght):
            
            population_length = self.population_lenght - 1
            
            guy1 = random.randint(0,population_length)
            guy2 = random.randint(0,population_length)
            
            cost1, cost2 = self.old_population[guy1][1], self.old_population[guy2][1] 
            if cost1 < cost2:
                self.current_population[i] = list(self.old_population[guy1])
            else:
                self.current_population[i] = list(self.old_population[guy2])  
        
    def cross(self):
        '''
        We need to cross `how_many_cross` individuals 
        with position based crossing operator
        '''
        
        for i in xrange(self.how_many_cross):
            parent1 = self.current_population[i][2]
            parent2 = self.current_population[i+1][2]
            
            child = [0] * self.n
            
            no_match = []
            index_no_match = []            
            for k in xrange(self.n):
                if parent1[k] == parent2[k]:
                    child[k] = parent1[k]
                else:
                    no_match.append(parent1[k])
                    index_no_match.append(k)
            
            random.shuffle(no_match)
            
            k = 0
            for j in index_no_match:
                child[j] = no_match[k]
                k += 1 
            # Add the child to the population and mark it as need to evaluate
            self.current_population[i][2] = list(child)
            self.current_population[i][0] = 1
    
    def mutate(self):
        '''
        Mutate a fraction of the population
        '''

        for _ in xrange(self.how_many_mutate):
            i = random.randint(0, self.population_lenght-1)
            j = random.randint(0, self.n-1)
            
            # Apply mutation to the gene
            y = random.randint(0, self.n-1)

            self.current_population[i][2][j],self.current_population[i][2][y] = self.current_population[i][2][y],self.current_population[i][2][j] 
            self.current_population[i][0] = 1 # Mark as need to evaluate
        
    def reemplace(self):
        '''
        Remplace the old population by the new following Elitists,
        if the best solution from the old population is lost,
        the worst in the current population is replaced by it.
        '''
        if self.best_guy not in self.current_population:
            # find the worst solution in current population an replace it
            pop_sort = list(self.current_population)
            pop_sort.sort(key=itemgetter(1))
            wort_guy = pop_sort[self.population_lenght-1]
            self.current_population[self.current_population.index(wort_guy)] = list(self.best_guy)
    
