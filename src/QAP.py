# -*- coding: utf-8 -*-

'''
Created on Mar 31, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''
import argparse

from qapproblem.BMB import BMB
from qapproblem.CompeticionPoblacional import CompeticionPoblacional
from qapproblem.Data import Data
from qapproblem.Elitist_GG_PMX import Elitist_GG_PMX
from qapproblem.Elitist_GG_pos import Elitist_GG_pos
from qapproblem.Grasp import Grasp
from qapproblem.Greedy import Greedy
from qapproblem.ILS import CompeticionTrayectorias
from qapproblem.LocalSearch import LocalSearch
from qapproblem.MA_10_01Best_PMX import MA_10_01Best_PMX
from qapproblem.MA_10_01_PMX import MA_10_01_PMX
from qapproblem.MA_10_1_PMX import MA_10_1_PMX
from qapproblem.SimulatedAnealling import SimulatedAnealling
from qapproblem.Stacionary_GG_PMX import Stacionary_GG_PMX
from qapproblem.Stacionary_GG_pos import Stacionary_GG_pos
from qapproblem.TabuSearch import TabuSearch


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
        ils = CompeticionTrayectorias(data, seed)
        if verbose:
            print 'Results for CompeticionTrayectorias, S=', ils.S , ' C(S)=' , ils.cost , ' seed=' , seed
        else:
            print ils.cost, '\t\t', ils.exec_time
    elif (algorithm == 'elitist_gg_pos'):
        agg = Elitist_GG_pos(data, seed)
        if verbose:
            print 'Results for elitist_gg_pos, S=', agg.S ,' C(S)=' , agg.cost , ' seed=' , seed
        else:
            print agg.cost, '\t\t', agg.exec_time
    elif (algorithm == 'elitist_gg_pmx'):
        agg = Elitist_GG_PMX(data, seed)
        if verbose:
            print 'Results for elitist_gg_pmx, S=', agg.S ,' C(S)=' , agg.cost , ' seed=' , seed
        else:
            print agg.cost, '\t\t', agg.exec_time
    elif (algorithm == 'stacionary_gg_pos'):
        agg = Stacionary_GG_pos(data, seed)
        if verbose:
            print 'Results for stacionary_gg_pos, S=', agg.S ,' C(S)=' , agg.cost , ' seed=' , seed
        else:
            print agg.cost, '\t\t', agg.exec_time
    elif (algorithm == 'stacionary_gg_pmx'):
        agg = Stacionary_GG_PMX(data, seed)
        if verbose:
            print 'Results for stacionary_gg_pmx, S=', agg.S ,' C(S)=' , agg.cost , ' seed=' , seed
        else:
            print agg.cost, '\t\t', agg.exec_time
    elif (algorithm == 'ma_10_1_pmx'):
        ma101 = MA_10_1_PMX(data, seed)
        if verbose:
            print 'Results for MA_10_1_PMX, S=', ma101.S ,' C(S)=' , ma101.cost , ' seed=' , seed
        else:
            print ma101.cost, '\t\t', ma101.exec_time
    elif (algorithm == 'ma_10_01_pmx'):
        ma1001 = MA_10_01_PMX(data, seed)
        if verbose:
            print 'Results for MA_10_01_PMX, S=', ma1001.S ,' C(S)=' , ma1001.cost , ' seed=' , seed
        else:
            print ma1001.cost, '\t\t', ma1001.exec_time
    elif (algorithm == 'ma_10_01best_pmx'):
        ma1001b = MA_10_01Best_PMX(data, seed)
        if verbose:
            print 'Results for MA_10_01Best_PMX, S=', ma1001b.S ,' C(S)=' , ma1001b.cost , ' seed=' , seed
        else:
            print ma1001b.cost, '\t\t', ma1001b.exec_time
    elif (algorithm == 'comppob'):
        compPob = CompeticionPoblacional(data, seed)
        if verbose:
            print 'Results for compPob, S=', compPob.S ,' C(S)=' , compPob.cost , ' seed=' , seed
        else:
            print compPob.cost, '\t\t', compPob.exec_time
    elif (algorithm == 'comptray'):
        comptray = CompeticionTrayectorias(data, seed)
        if verbose:
            print 'Results for comptray, S=', comptray.S ,' C(S)=' , comptray.cost , ' seed=' , seed
        else:
            print comptray.cost, '\t\t', comptray.exec_time

    elif (algorithm == 'ts'):
        ts = TabuSearch(data, seed)
        print 'Results for Tabu Search, S=', ts.S , ' C(S)=' , ts.cost , ' seed=' , seed
    else:
        print 'Argumentos inválidos'

if __name__ == '__main__':
    main()
