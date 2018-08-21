#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 21:11:31 2018

@author: matias
"""

import scipy as sp
import matplotlib.pyplot as plt
import os
import time

start_time = time.time()

g = 9.806 # m/(s**2)
BMetadatos = []
Dir = "/home/matias/Mis Documentos/UAndes/Métodos Computacionales en OOCC/Tareas/Proyecto 1/Registros Sismológicos/Seleccionados/"  # Directorio donde se encuentran los 30 sismos que cumplen el criterio.
seleccionados = os.listdir(Dir)

# -----------------------------------------------------------------------------

for j, arch in enumerate(seleccionados):
    archivo = open(Dir+arch)
    Ti = archivo.readline()[-28:]
    TiD = {'año':Ti[:4], 'mes':Ti[5:7], 'dia':Ti[8:10], 'hora':Ti[11:13], 'min':Ti[14:16], 'seg':Ti[17:19], 'mseg':Ti[20:-2]}
    tasam = float(archivo.readline()[20:25])
    Nmuestras = float(archivo.readline()[-6:])
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
    L6 = archivo.readline()
    L7 = archivo.readline()
    latitudHipo = float(L7[16:21])
    longitudHipo = float(L7[-8:])
    profundidad = int(archivo.readline()[-3:])
    magnitud = float(archivo.readline()[-4:])
    archivo.close()
    
# -----------------------------------------------------------------------------
    
    a = sp.loadtxt(Dir+arch)
    dt = 1./Nmuestras
    Nt = a.size
    v = sp.zeros(Nt)
    d = sp.zeros(Nt)
    v[1:] = sp.cumsum(a[1:] + a[0:-1])*dt/2
    d[1:] = sp.cumsum(v[1:] + v[0:-1])*dt/2
    t = sp.arange(0, dt*Nt, dt)
    Ia = sp.zeros(Nt)
    a2 = a**2
    da2 = (a2[0:-1] + a2[1:])*dt/2     
    Ia[1:] = sp.cumsum(da2)*sp.pi/(2*g)     
    Ia_inf = Ia.max()     
    i_05 = sp.argmin(abs(Ia - 0.05*Ia_inf))
    i_95 = sp.argmin(abs(Ia - 0.95*Ia_inf))     
    t_05 = t[i_05]
    Ia_05 = Ia[i_05]     
    t_95 = t[i_95]
    Ia_95 = Ia[i_95]     
    D_5_95 = t_95 - t_05
    PGA = max(abs(a))
    al = sp.ndarray.tolist(a)
    i_PGA = sp.argmax(abs(a))
    PGA = (a[i_PGA])/g
    i_PGV = sp.argmax(abs(v))
    PGV = (v[i_PGV])
    i_PGD = sp.argmax(abs(d))
    PGD = (d[i_PGD])
    
# ----------------------------------------------------------------------------- 
    
    metadatos = {'Fecha': TiD['año']+TiD['mes']+TiD['dia'],
                 'Hora': TiD['hora']+':'+TiD['min']+':'+TiD['seg'],
                 'Epi_Lat': latitudHipo,
                 'Epi_Lon': longitudHipo,
                 'Epi_Profundidad': profundidad,
                 'M': magnitud,
                 'Estacion_Lat': latitudEst,
                 'Estacion_Lon': longitudEst,
                 'Estacion_Nombre': estacion,
                 'Componente': componente,
                 'PGA': PGA,
                 'PGV': PGV,
                 'PGD': PGD,
                 'Duracion': D_5_95
                 }
    Metadatos = {'a': 0, 't': 0, 'metadatos':{}}
    Metadatos('a') = a
    Metadatos('t') = t
    Metadatos('metadatos') = metadatos
    BMetadatos.append(Metadatos)

# -----------------------------------------------------------------------------
   
    plt.figure(j+1)
    ax1=plt.subplot(3,2,1)
    plt.grid()
    plt.axis(ymin=-0.6, ymax=0.6)
    plt.xlabel('Tiempo, $\it{t}$ (s)')
    plt.ylabel('Acc, $\it{a}$ (g)')
    plt.plot(t,a/g)
    plt.plot(t[i_PGA],PGA, 'or')
    ax1.annotate('PGA = '+str(round(PGA,3)), xy=(t[i_PGA], PGA), xytext=(t[i_PGA]+5, PGA))
    plt.axvline(t_05, ls='--', color='k')
    plt.axvline(t_95, ls='--', color='k')
    
    ax2=plt.subplot(3,2,3)
    plt.grid()
    plt.xlabel('Tiempo, $\it{t}$ (s)')
    plt.ylabel('Vel, $\it{v}$ (cm/s)')
    plt.plot(t,v)
    plt.plot(t[i_PGV],PGV, 'or')
    ax2.annotate('PGV = '+str(round(PGV,3)), xy=(t[i_PGV], PGV), xytext=(t[i_PGV]+5, PGV))
    plt.axvline(t_05, ls='--', color='k')
    plt.axvline(t_95, ls='--', color='k')
    
    ax3=plt.subplot(3,2,5)
    plt.grid()
    plt.xlabel('Tiempo, $\it{t}$ (s)')
    plt.ylabel('Dist, $\it{d}$ (cm)')
    plt.plot(t,d)
    plt.plot(t[i_PGD],PGD, 'or')
    ax3.annotate('PGD = '+str(round(PGD,3)), xy=(t[i_PGD], PGD), xytext=(t[i_PGD]+5, PGD))
    plt.axvline(t_05, ls='--', color='k')
    plt.axvline(t_95, ls='--', color='k')
    
    plt.subplot(1,2,2)
    plt.grid()
    plt.xlabel('Tiempo, $\it{t}$ (s)')
    plt.plot(t,Ia)
    plt.axvline(t_05, ls='--', color='k')
    plt.axvline(t_95, ls='--', color='k')
    plt.title("$D_{{5-95}} = {}s$".format(round(D_5_95,4)))
    
    plt.suptitle('Evento: '+arch[:-4])
    plt.show()

# -----------------------------------------------------------------------------

for j,i in enumerate(BMetadatos):
    sp.savez("$registro_{}$".format(str(j+1).zfill(2)), a=i['a'], t=i['t'], metadatos=i['metadatos'])

# -----------------------------------------------------------------------------

print("--- Terminado en %s seg. ---" % (time.time() - start_time))
