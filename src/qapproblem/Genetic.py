'''
Created on Apr 30, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''

import math
from operator import itemgetter
from random import randint
from random import shuffle

from qapproblem.Heuristic import Heuristic

class GG_Base(Heuristic):
    '''
    Base Class for Genetic Algorithm
    '''
    population_lenght = 50
    cross_prob = .7 # 1 for EGG
    mutation_prob = .01
    stop_crit = 20000
    how_many_cross = int(math.ceil(cross_prob * (population_lenght / 2)))
    
    current_population = []
    old_population = [0] * population_lenght
    best_current_cost = 10 ** 10
    best_guy = []
    index_best_guy = 0
    
    def __init__(self, f_name, seed):
        super(GG_Base, self).__init__(f_name, seed)
        
        self.n = self._tam
        self.num_genes = self.population_lenght * self.n 
        # How many will mutate (genes per individual  * num individual * prob mutation) 
        self.how_many_mutate = int(math.ceil(self.num_genes * self.mutation_prob))                    
        
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
        
        for i in xrange(self.population_lenght):
            p = population[i]
            if p[0]:  # need to re-evaluate
                p[1] = C(p[2])
                self.stop_crit -= 1
                p[0] = 0  # mark it as evaluated
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

            i_guy1 = randint(0, population_length)
            i_guy2 = randint(0, population_length)
            
            guy1 = self.old_population[i_guy1]
            guy2 = self.old_population[i_guy2]
            
            while guy1 == guy2:
                i_guy2 = randint(0, population_length)
                guy2 = self.old_population[i_guy2]
            
            cost1, cost2 = guy1[1], guy2[1] 

            if cost1 < cost2:
                self.current_population[i] = list(guy1)
            else:
                self.current_population[i] = list(guy2)  
    
    def mutate(self):
        '''
        Mutate a fraction of the population
        '''
        for _ in xrange(self.how_many_mutate):
            i = randint(0, self.population_lenght - 1)
            j = randint(0, self.n - 1)
            
            # Apply mutation to the gene
            y = randint(0, self.n - 1)

            self.current_population[i][2][j], self.current_population[i][2][y] = self.current_population[i][2][y], self.current_population[i][2][j] 
            self.current_population[i][0] = 1  # Mark as need to evaluate
        
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
            wort_guy = pop_sort[self.population_lenght - 1]
            self.current_population[self.current_population.index(wort_guy)] = list(self.best_guy)
    
    def get_two_childs(self, p1, p2):
        '''
        Returns two childs for the two parents selected by tournament
        '''
        childs = []
        
        child = [0] * self.n
        no_match = []
        index_no_match = []    
                
        for k in xrange(self.n):
            if p1[k] == p2[k]:
                child[k] = p1[k]
            else:
                no_match.append(p1[k])
                index_no_match.append(k)
                
        clean_child = list(child)  # A list with only matching items from parents
        
        append_child = childs.append
        if no_match:
            for _ in xrange(2):
                old_n_match = list(no_match)
                shuffle(no_match)
                # We do not want two children be the same
                while old_n_match == no_match:
                    shuffle(no_match)
                    
                k = 0
                for j in index_no_match:
                    child[j] = no_match[k]
                    k += 1
                    
                append_child(child)
                child = list(clean_child)
        else:
            # The children are the same as the parent
            append_child(-1)
            append_child(-1)
            
        return childs
