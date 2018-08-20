#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 18:23:30 2018

@author: matias
"""

import scipy as sp
import os
import shutil
import time

start_time = time.time()


g = 9.81   # m/(s**2)

def enlistar(ruta):    
    sel = []
    for i in os.listdir(ruta):
        a = sp.loadtxt(ruta+'/'+i)
        if max(abs(a)) >= 0.35*g and max(abs(a)) <= 0.55*g:
            sel.append(i)
        if len(sel) >= 30:
            break
    return sel

Dir0 = "/home/matias/Mis Documentos/UAndes/Métodos Computacionales en OOCC/Tareas/Proyecto 1/Registros Sismológicos/"

Gen = [['HNE/', enlistar(Dir0+"HNE")],
       ['HNN/', enlistar(Dir0+"HNN")],
       ['HNZ/', enlistar(Dir0+"HNZ")],
       ['HLE/', enlistar(Dir0+"HLE")],
       ['HLN/', enlistar(Dir0+"HLN")],
       ['HLZ/', enlistar(Dir0+"HLZ")]]

for lista in Gen:
    for i in lista[1]:
        shutil.copy(Dir0+lista[0]+i, Dir0+'S_'+lista[0]+i)


print ''
print("--- Terminado en %s seg. ---" % (time.time() - start_time))


