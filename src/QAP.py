# -*- coding: utf-8 -*-

'''
Created on Mar 31, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''
import argparse

from qapproblem.Greedy import Greedy
from qapproblem.LocalSearch import LocalSearch


def main(): 
    
    parser = argparse.ArgumentParser(description='QAP Problem')
    parser.add_argument('-d','--data_file', help='File with the problem data',type=str, required=True)
    parser.add_argument('-a', '--algorithm', help='Algorithm to use', type=str, required=True)
    parser.add_argument('-v','--verbose', help='Show debug info', action='store_true', default=False, required=False)

    args = parser.parse_args()
    
    data_file = args.data_file
    algorithm =  args.algorithm.strip().lower()
    
    if (algorithm == 'greedy'):
        greedy = Greedy(data_file)
        print 'Results for Greedy, S = ', greedy.cost , ' C(S) = ' , greedy.S
    elif (algorithm == 'local_search'):
        ls = LocalSearch(data_file)
        print 'Results for Local Search, S = ', ls.cost , ' C(S) ' , ls.S
    else:
        print 'Argumentos inválidos'
    
if __name__ == '__main__':
    main()
