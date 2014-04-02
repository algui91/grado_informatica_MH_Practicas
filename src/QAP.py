# -*- coding: utf-8 -*-

'''
Created on Mar 31, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''
import argparse

from qapproblem.Greedy import Greedy


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
        print 'Cost of solution for Greedy: ', greedy.cost , ' with permutation %s ' % greedy.S
    else:
        print 'Argumentos inválidos'
    
if __name__ == '__main__':
    main()