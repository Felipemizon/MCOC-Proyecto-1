#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 18:23:30 2018

@author: matias
"""

import scipy as sp
from os import listdir
import time

start_time = time.time()


g = 9.81   # m/(s**2)

def enlistar(ruta):    
    sel = []
    for i in listdir(ruta):
        a = sp.loadtxt(ruta+'/'+i)
        if max(abs(a)) >= 0.35*g and max(abs(a)) <= 0.55*g:
            sel.append(i)
        if len(sel) >= 30:
            break
    return sel

HNE = enlistar("/home/matias/Mis Documentos/UAndes/Métodos Computacionales en OOCC/Tareas/Proyecto 1/Registros Sismológicos/HNE")
HNN = enlistar("/home/matias/Mis Documentos/UAndes/Métodos Computacionales en OOCC/Tareas/Proyecto 1/Registros Sismológicos/HNN")
HNZ = enlistar("/home/matias/Mis Documentos/UAndes/Métodos Computacionales en OOCC/Tareas/Proyecto 1/Registros Sismológicos/HNZ")

HLE = enlistar("/home/matias/Mis Documentos/UAndes/Métodos Computacionales en OOCC/Tareas/Proyecto 1/Registros Sismológicos/HLE")
HLN = enlistar("/home/matias/Mis Documentos/UAndes/Métodos Computacionales en OOCC/Tareas/Proyecto 1/Registros Sismológicos/HLN")
HLZ = enlistar("/home/matias/Mis Documentos/UAndes/Métodos Computacionales en OOCC/Tareas/Proyecto 1/Registros Sismológicos/HLZ")


print 'HNE: ', HNE
print 'HNN: ', HNN
print 'HNZ: ', HNZ

print ''

print 'HLE: ', HLE
print 'HLN: ', HLN
print 'HLZ: ', HLZ


print ''
print("--- Terminado en %s seg. ---" % (time.time() - start_time))
