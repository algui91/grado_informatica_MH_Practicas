# -*- coding: utf-8 -*-

'''
Created on Jul 13, 2014

@author Alejandro Alcalde (elbauldelprogramador.com)

Licensed Under GPLv3
'''
import argparse
import fnmatch
import os

from qapproblem.Data import Data
from qapproblem.Heuristic import Heuristic


def main():
    
    parser = argparse.ArgumentParser(description='QAP Problem solution tester')
    parser.add_argument('-d', '--solution_directory', help='Directory containing solutions', type=str, required=True)

    args = parser.parse_args()

    folder = args.solution_directory

    for solution_file in os.listdir(folder):
        if fnmatch.fnmatch(solution_file, '*.sln'):
            with open(os.path.join(folder, solution_file), 'r') as fp:
                dat = map(int,fp.read().split())
                print 'Solución para instancia: ', solution_file
                print '\t Tamaño problema', dat[0]
                print '\t Coste del fichero: ', dat[1]
                #print '\t\t Solución: ', dat[2:]
                print '\t Calculando coste... ',
                filename = os.path.join(folder, os.path.splitext(solution_file)[0] + '.dat')
                values = Data(filename) 
                #h = Heuristic(values, 0)
                cost =  C(dat[0], values, dat[2:]) #h.C(S=dat[2:])
                print '¿Coincide? ', cost , ' == ', dat[1]
                print '\t TEST PASADO: ', cost == dat[1]

def C(_tam, _data, s):
    '''
    Cost of the solution with permutation S
    Hay que contar el número de búsquedas, limitado a 10000
    '''
    cost = 0
    
    for i in xrange(_tam):
        for j in xrange(_tam):
            cost += _data.stream_matrix[i][j] * _data.distance_matrix[s[i]][s[j]]

    return cost

if __name__ == '__main__':
    main()