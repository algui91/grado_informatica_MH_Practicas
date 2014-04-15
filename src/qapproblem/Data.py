'''
Created on Apr 1, 2014

@author: Alejandro Alcalde (elbauldelprogramador.com)

Licensed under GPLv3
'''

class Data:
    '''
    Class representing a QAP problem data, with the two matrix representing
    distances and streams between each unit
    '''

    distance_matrix = []
    stream_matrix = []
    file_name = ''
    tam = 0

    def __init__(self, f_name):
        '''
        Read f_name to matrix from file
        '''
        #print 'Reading data from %s' % f_name
        self.file_name = f_name
        self._load_data()
        
    def _load_data(self):
        with open(self.file_name, 'r') as fp:
            dat = map(int,fp.read().split())
        self.tam = dat.pop(0)

        tam_dat = len(dat)
        half_tam_dat = tam_dat >> 1
        
        self.distance_matrix = self._chunks(0, half_tam_dat, self.tam, dat)
        self.stream_matrix = self._chunks(half_tam_dat, tam_dat, self.tam, dat)
        
    def _chunks(self, start, stop, n, l):
        '''
        Return successive n-sized chunks from l.
        @param start: Index from where to start
        @param stop: Index from where to stop
        @param n: n-sized chunk for row
        @param l: List from where extract data
        '''
        row = []
        for i in xrange(start, stop, n):
            row.append(l[i:i+n])
            
        return row
