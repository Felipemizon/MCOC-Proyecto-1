#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 21:11:31 2018

@author: matias
"""

from datetime import datetime, timedelta
import scipy as sp
import matplotlib.pyplot as plt
from os import listdir
import time

start_time = time.time()

def datetime_range(start, samples, delta):
    cont = 0
    current = start
    while True:
        yield current
        current += delta
        cont += 1
        if cont >= samples:
            break


Metadatos = []


Dir = "/home/matias/Mis Documentos/UAndes/Métodos Computacionales en OOCC/Tareas/Proyecto 1/Registros Sismológicos/Seleccionados"

seleccionados = listdir(Dir)

for j, arch in enumerate(seleccionados):
    archivo = open(arch)
    Ti = archivo.readline()[-28:]
    TiD = {'año':Ti[:4], 'mes':Ti[5:7], 'dia':Ti[8:10], 'hora':Ti[11:13], 'min':Ti[14:16], 'seg':Ti[17:19], 'mseg':Ti[20:-2]}
    tasam = float(archivo.readline()[20:25])
    Nmuestras = int(archivo.readline()[-6:])
    L4 = archivo.readline()
    estacion = L4[12:16]
    if L4[-2] == 'E':
        componente = 'EW'
    elif L4[-2] == 'N':
        componente = 'NS'
    elif L4[-2] == 'Z':
        componente = 'Z'
    L5 = archivo.readline()
    latitudEst = float(L5[11:18])
    longitudEst = float(L5[-8:])
    archivo.close()
        
    a = sp.loadtxt(arch)
    
    t = [dt.strftime('%H:%M:%S.%fZ Z') for dt in 
         datetime_range(datetime(int(TiD['año']), int(TiD['mes']), int(TiD['dia']), int(TiD['hora']), int(TiD['min']), int(TiD['seg']), int(TiD['mseg'])), Nmuestras, 
         timedelta(seconds=tasam/60))]
    
    metadatos = {'Fecha': TiD['año']+TiD['mes']+TiD['dia'],
                 'Hora': TiD['hora']+':'+TiD['min']+':'+TiD['seg'],
                 'Estacion_Lat': latitudEst,
                 'Estacion_Lon': longitudEst,
                 'Estacion_Nombre': estacion,
                 'Componente': componente
                 }
    Metadatos.append(metadatos)
        
    plt.figure(j)
    plt.title('Evento: '+Ti)
    plt.plot(a)



