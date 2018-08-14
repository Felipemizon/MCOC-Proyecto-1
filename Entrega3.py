#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 19:56:46 2018

@author: matias
"""

import scipy as sp
from scipy.sparse import spdiags

##########################################################################################
# Unidades:
N = 1           # Newton
kg = 1          # Kilogramos
s = 1           # Segundos
Pa = kg*N/s     # Pascales

GPa = Pa*1e9
ton = kg*1e3
##########################################################################################

n = 20

E = 23.5*GPa
I = [(0.6**4)/12, (0.7**4)/12, (0.8**4)/12, (0.9**4)/12, (1**4)/12] # Inercias de 60x60 (2.8m)

Kcolumnas1 = [] #Rigidez de columnas 60x60,70x70... 4m de alto
Kcolumnas2 = [] #Rigidez de columnas 60x60,70x70... 2.8m de alto
kk = sp.zeros(6)

for Ic in I:
    Kcolumnas1.append(12.*E*Ic/(4**3))
    Kcolumnas2.append(12.*E*Ic/(2.8**3))

combcolum = [[6,2,0,1,4],[4,0,1,0,4],[0,0,1,4,0],[0,1,4,0,0],[5,0,0,0,0]]

k1 = 0
for i in range(5):
    k1 += Kcolumnas1[i]*combcolum[0][i]   
kk[0] = k1

k2 = 0
for j in range(5):
    for i in range(5):
        k2 += Kcolumnas2[i]*combcolum[j][i]    
    kk[j+1] = k2
    k2 = 0

k = sp.zeros(n)
for i in range(n):
    k[0] = kk[0]
    if i > 0 and i <= 3:
        k[i] = kk[1]
    elif i > 3 and i <= 7:
        k[i] = kk[2]
    elif i > 7 and i <= 11:
        k[i] = kk[3]
    elif i > 11 and i <= 15:
        k[i] = kk[4]
    elif i > 15 and i <= 19:
        k[i] = kk[5]

d1 = sp.ones(n)
d = sp.vstack((d1, d1, d1))
K = sp.asarray(spdiags(d, (-1, 0, 1), n, n).todense())

K = -k*K

for i in range(n-1):
    K[i,i] = k[i]+k[i+1]    
K[-1,-1] = k[-1]