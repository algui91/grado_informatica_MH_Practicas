'''
Created on Mar 31, 2014

@author: Alejandro Alcalde
'''

data_path = 'data/'

def greedy():
    
    matrixA = []
    
    with open(data_path + 'els19.dat', 'r') as fp:
        # Consume values that we do not need
        fp.next()
        fp.next()
        for line in fp:
            matrixA.append(matrixA.append([int(x) for x in line.split()]))
    print matrixA
if __name__ == '__main__':
    greedy()