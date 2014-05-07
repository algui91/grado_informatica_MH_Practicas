# -*- coding: utf-8 -*-

'''
Created on Mar 31, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''
import argparse

from qapproblem.BMB import BMB
from qapproblem.Data import Data
from qapproblem.Grasp import Grasp
from qapproblem.Greedy import Greedy
from qapproblem.LocalSearch import LocalSearch
from qapproblem.SimulatedAnealling import SimulatedAnealling
from qapproblem.TabuSearch import TabuSearch
from qapproblem.ILS import ILS


def main(): 
    
    parser = argparse.ArgumentParser(description='QAP Problem')
    parser.add_argument('-d', '--data_file', help='File with the problem data', type=str, required=True)
    parser.add_argument('-a', '--algorithm', help='Algorithm to use', type=str, required=True)
    parser.add_argument('-s', '--seed', help='Seed to use for randomly generated initial solutions', type=int, required=True)
    parser.add_argument('-v', '--verbose', help='Show debug info', action='store_true', default=False, required=False)

    args = parser.parse_args()
    
    data_file = args.data_file
    algorithm = args.algorithm.strip().lower()
    verbose = args.verbose
    seed = args.seed
    
    data = Data(data_file)
    
    if (algorithm == 'greedy'):
        greedy = Greedy(data, seed)
        if verbose:
            print 'Results for Greedy, S=', greedy.cost , ' C(S)=' , greedy.S , ' seed=' , seed
        else:
            print greedy.cost, '\t\t', greedy.exec_time  # , data_file, seed
    elif (algorithm == 'local_search'):
        ls = LocalSearch(data, seed)
        if verbose:
            print 'Results for Local Search, S=', ls.S , ' C(S)=' , ls.cost , ' seed=' , seed
        else:
            print ls.cost, '\t\t', ls.exec_time  # , data_file, seed
    elif (algorithm == 'sa'):
        sa = SimulatedAnealling(data, seed)
        if verbose:
            print 'Results for Simulated Annealing, S=', sa.S , ' C(S)=' , sa.cost , ' seed=' , seed
        else:
            print sa.cost, '\t\t', sa.exec_time  # , data_file, seed
    elif (algorithm == 'bmb'):
        bmb = BMB(data, seed)
        if verbose:
            print 'Results for BMB, S=', bmb.S , ' C(S)=' , bmb.cost , ' seed=' , seed
        else:
            print bmb.cost, '\t\t', bmb.exec_time
    elif (algorithm == 'grasp'):
        grasp = Grasp(data, seed)
        if verbose:
            print 'Results for GRASP, S=', grasp.S , ' C(S)=' , grasp.cost , ' seed=' , seed
        else:
            print grasp.cost, '\t\t', grasp.exec_time
    elif (algorithm == 'ils'):
        ils = ILS(data, seed)
        if verbose:
            print 'Results for ILS, S=', ils.S , ' C(S)=' , ils.cost , ' seed=' , seed
        else:
            print ils.cost, '\t\t', ils.exec_time
    elif (algorithm == 'ts'):
        ts = TabuSearch(data, seed)
        print 'Results for Tabu Search, S=', ts.S , ' C(S)=' , ts.cost , ' seed=' , seed
    else:
        print 'Argumentos inválidos'
    
if __name__ == '__main__':
    main()
