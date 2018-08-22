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
#A continuacion se almacena en una variable los sismos que se descargaron y que cumplen con los supuestos estipulados en el enunciado
g = 9.806 # m/(s**2)
BM = []
Dir = "/home/matias/Mis Documentos/UAndes/Métodos Computacionales en OOCC/Tareas/Proyecto 1/Registros Sismológicos/Seleccionados/"  # Directorio donde se encuentran los 30 sismos que cumplen el criterio.
seleccionados = os.listdir(Dir)
seleccionados.sort()

# -----------------------------------------------------------------------------
#Se procede a guardar las variables para luego crear un diccionario con el año, mes, dia, etc
for arch in seleccionados:
    archivo = open(Dir+arch)
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
    L6 = archivo.readline()
    L7 = archivo.readline()
    latitudHipo = float(L7[16:21])
    longitudHipo = float(L7[-8:])
    profundidad = int(archivo.readline()[-3:])
    magnitud = float(archivo.readline()[-4:])
    archivo.close()
    
# -----------------------------------------------------------------------------
# Se almacenan en variables aceleracion, velocidad y desplazamiento maximo, ademas de generar un vector tiempo que ser necesario para crear luego un diccionario      
    a = sp.loadtxt(Dir+arch) 
    dt = 1./tasam  
    t = sp.arange(0, dt*Nmuestras, dt)    
    Ia = sp.zeros(Nmuestras)     
    a2 = a**2
    da2 = (a2[0:-1] + a2[1:])*dt/2    
    v = sp.zeros(Nmuestras)
    d = sp.zeros(Nmuestras)     
    v[1:] = 100*sp.cumsum(a[1:] + a[0:-1])*dt/2
    d[1:] = sp.cumsum(v[1:] + v[0:-1])*dt/2     
    Ia[1:] = sp.cumsum(da2)*sp.pi/(2*g)     
    Ia_inf = Ia.max()     
    i_05 = sp.argmin(abs(Ia - 0.05*Ia_inf))
    i_95 = sp.argmin(abs(Ia - 0.95*Ia_inf))     
    t_05 = t[i_05]
    Ia_05 = Ia[i_05]     
    t_95 = t[i_95]
    Ia_95 = Ia[i_95]     
    D_5_95 = t_95 - t_05
    i_PGA = sp.argmax(abs(a))
    PGA = (a[i_PGA])/g     
    i_PGV = sp.argmax(abs(v))
    PGV = (v[i_PGV])     
    i_PGD = sp.argmax(abs(d))
    PGD = (d[i_PGD])    
    if len(t)>len(a) or len(t)>len(v) or len(t)>len(d):
        t = sp.delete(t,0)
    
# ----------------------------------------------------------------------------- 
 #A partir de lo creado anteriormente, se genera el diccionario   
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
    Metadatos = {}
    Metadatos['a'] = a
    Metadatos['t'] = t
    Metadatos['metadatos'] = metadatos
    BM.append(Metadatos)

# -----------------------------------------------------------------------------
  #Codigo generado para graficar  
    plt.figure()
    plt.subplot(3,2,1)
    plt.grid()
    plt.ylim([-0.6,0.6])
    plt.xlabel('Tiempo, $\it{t}$ (s)')
    plt.ylabel('Acc, $\it{a}$ (g)')
    plt.plot(t,a/g)
    plt.plot(t[i_PGA],PGA, 'or')
    plt.text(t[i_PGA],PGA, "PGA={0:0.3f}g".format(abs(PGA)))
    plt.axvline(t_05, ls='--', color='k')
    plt.axvline(t_95, ls='--', color='k')
    
    plt.subplot(3,2,3)
    plt.grid()
    plt.ylim([-15,15])
    plt.xlabel('Tiempo, $\it{t}$ (s)')
    plt.ylabel('Vel, $\it{v}$ (cm/s)')
    plt.plot(t,v)
    plt.plot(t[i_PGV],PGV, 'or')
    plt.text(t[i_PGV],PGV, "PGV={0:0.3f}cm/s".format(abs(PGV)))
    plt.axvline(t_05, ls='--', color='k')
    plt.axvline(t_95, ls='--', color='k')
    
    plt.subplot(3,2,5)
    plt.grid()
    plt.ylim([-15,15])
    plt.xlabel('Tiempo, $\it{t}$ (s)')
    plt.ylabel('Dist, $\it{d}$ (cm)')
    plt.plot(t,d)
    plt.plot(t[i_PGD],PGD, 'or')
    plt.text(t[i_PGD],PGD, "PGD={0:0.3f}cm".format(abs(PGD)))
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

for j,i in enumerate(BM):
    sp.savez("registro_{}".format(str(j+1).zfill(2)), a=i['a'], t=i['t'], metadatos=i['metadatos'])

# -----------------------------------------------------------------------------

print("--- Terminado en %s seg. ---" % (time.time() - start_time))

