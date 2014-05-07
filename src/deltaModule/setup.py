#!/usr/bin/env python

from distutils.core import setup, Extension

SRC = 'src/'

module1 = Extension('delta',
                    #extra_compile_args = ['-O2', '-std=gnu99'],
                    extra_compile_args = ['-O0', '-std=gnu99', '-g', '-Wall'],
                    sources = [SRC + 'delta.c'])

setup (name = 'Delta',
       version = '0.1',
       description = 'Delta - Graphic Network Monitoring tool',
       author = 'Alejandro Alcalde',
       author_email = 'algui91@gmail.com',
       url = 'https://github.com/algui91/GraphicNetworkMonitoring',
       license = 'GPLv3',
       long_description = '''
       TODO
       ''',
       ext_modules = [module1])
