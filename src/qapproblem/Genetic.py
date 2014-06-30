'''
Created on Apr 30, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''

from copy import deepcopy
import itertools
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

    worst_current_cost1 = 0
    worst_guy1 = []
    index_worst_guy1 = 0
    worst_current_cost2 = 0
    worst_guy2 = []
    index_worst_guy2 = 0

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

    def evaluate(self, popupation_l, new_gen=None):
        '''
        Evaluate the population
        '''
        population = new_gen if new_gen != None else self.current_population
        C = self.C

        for i in xrange(popupation_l):
            p = population[i]
            if p[0]:  # need to re-evaluate
                p[1] = C(p[2])
                self.stop_crit -= 1
                p[0] = 0  # mark it as evaluated
            if p[1] < self.best_current_cost:
                self.best_guy = p
                self.best_current_cost = p[1]
                self.index_best_guy = i

        self.index_worst_guy1, self.index_worst_guy2 = self.get_index_worst_guy_n(1,2)

    def select(self, tournament_number, stacionary=False):
        '''
        Select two individuals by tournament
        '''
        population_length = self.population_lenght - 1

        for i in xrange(tournament_number):

            i_guy1 = randint(0, population_length)
            i_guy2 = randint(0, population_length)

            # If deepcopy consumes much time, copy list with :
            guy1 = deepcopy(self.old_population[i_guy1])
            guy2 = deepcopy(self.old_population[i_guy2])

            while guy1 == guy2:
                i_guy2 = randint(0, population_length)
                guy2 = deepcopy(self.old_population[i_guy2])
                if len(list(k for k,_ in itertools.groupby(self.current_population))) == 1:
                    self.current_population = []
                    self.initPopulation()

            cost1, cost2 = guy1[1], guy2[1]

            if cost1 < cost2:
                self.current_population[i] = list(guy1)
            else:
                self.current_population[i] = list(guy2)

        if stacionary:
            return [list(guy1), list(guy2)]

    def mutate(self, population_l, how_many, new_gen=None):
        '''
        Mutate a fraction of the population
        '''
        if new_gen:
            population = new_gen
        else:
            population = self.current_population

        for _ in xrange(how_many):
            i = randint(0, population_l - 1)
            j = randint(0, self.n - 1)

            # Apply mutation to the gene
            y = randint(0, self.n - 1)

            population[i][2][j], population[i][2][y] = population[i][2][y], population[i][2][j]
            population[i][0] = 1  # Mark as need to evaluate

    def reemplace(self):
        '''
        Remplace the old population by the new following Elitists,
        if the best solution from the old population is lost,
        the worst in the current population is replaced by it.
        '''
        if self.best_guy not in self.current_population:
            self.current_population[self.get_index_worst_guy_n(1)[0]] = deepcopy(self.best_guy)

    def get_index_worst_guy_n(self, *n):
        '''
        @param *n: The index of the nth worst guys
        '''
        population = self.current_population
        pop_sort = list(population)
        pop_sort.sort(key=itemgetter(1))

        return [population.index(pop_sort[-i]) for i in n]

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
