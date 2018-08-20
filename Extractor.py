#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 18:58:31 2018

@author: calocha
"""

import zipfile
from os import listdir

Dir1 = "/home/matias/Mis Documentos/UAndes/Métodos Computacionales en OOCC/Tareas/Proyecto 1/Registros Sismológicos/"
Dir2 = "Zips/"

sismos = listdir(Dir1+Dir2)

for arch in sismos:
    zipf = zipfile.ZipFile(Dir1+Dir2+arch)
    contents = zipf.namelist()
    for i,j in enumerate(contents):
        final = contents[i][-7:]
        if final == 'HNE.txt':
            zipf.extract(contents[i], path=Dir1+"HNE")
        elif final == 'HNN.txt':
            zipf.extract(contents[i], path=Dir1+"HNN")
        elif final == 'HNZ.txt':
            zipf.extract(contents[i], path=Dir1+"HNZ")
        elif final == 'HLE.txt':
            zipf.extract(contents[i], path=Dir1+"HLE")
        elif final == 'HLN.txt':
            zipf.extract(contents[i], path=Dir1+"HLN")
        elif final == 'HLZ.txt':
            zipf.extract(contents[i], path=Dir1+"HLZ")
        
    


