#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 19:11:21 2018

@author: matias
"""

# Librerias
import scipy as sp
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import scipy.interpolate as interpol

###############################################################################
###############################################################################
# EDIFICIO
# Importar datos edificio
data1 = sp.load('mck.npz')
M = data1['M']
C = data1['C']
K = data1['K']
Mi = sp.array(sp.matrix(M).I)
# Capacidad disipadores
cs = sp.array([150.,250.,500.,800.])*1000    #N, capacidades disponibles
Cap = sp.array([0,cs[3],cs[1],cs[2],2*cs[0],cs[3],0,2*cs[0],cs[1],cs[0],cs[2],0,2*cs[0],cs[0],2*cs[0],cs[1],cs[1],cs[0],cs[0],cs[0]])        #cantidad de disipadores y que tipo por piso

###############################################################################
###############################################################################
# PARAMETROS Y FUNCIONES
#Parametros
vr = 0.001              # [m/s] Velocidad de referencia para la aproximacion de la friccion via tanh.
dt = 0.001              # [s]   Paso de integracion a usar

# Matriz de estado A
A = sp.block([[sp.zeros((20,20)),sp.eye(20)],
              [-Mi*K,-Mi*C]])
# Interpolador
def interpolado(a, dt, graficar=False):
    Na = a.size
    dt = 1/dt
    t = sp.arange(0,Na*dt,dt)  
    a_interpolado = interpol.interp1d(t, a, kind="cubic")
    ia = a_interpolado(t)
    if graficar==True:
        plt.plot(t,a,'o', t,ia,'-')
        plt.show()
    return a_interpolado

# Funcion del lado derecho de la EDO (de primer orden)
# a resolver zp = fun(t,z).  zp es la derivada temporal de z.
def fun(t,z):
    # --- Reporte de paso de tiempo
    if t > fun.tnextreport:
        print "  {} at t = {}".format(fun.solver, fun.tnextreport)
        fun.tnextreport += 1
    # --- Cálculo
    Famort = sp.zeros((40))   # vector de fuerza friccional de amortiguamiento
    Famort[0] = -(Cap[0] * (1./M[0,0]) * sp.tanh((z[20]/vr)))    
    Ft=sp.zeros(40)
    if t<226.81:
        Ft[20:]=f0(t)*9.8
    return sp.matmul(A,z) + Famort + Ft

###############################################################################
###############################################################################
# DESARROLLO

   ############################################################################
# REGISTROS
# Importar datos registros
data2 = sp.load('registro_01.npz')
a = data2['a']
t1 = data2['t']
dt1 = round(t1[3]-t1[2], 3)
tmax = max(t1)*1.1      # [s]   Tiempo maximo de integracion

f0 = interpolado(a,dt1)
t = sp.arange(0, tmax, dt)
Nt = len(t)
   ############################################################################

#Inicializar una matriz z para guardar las solucion discretizada
z_euler = sp.zeros((40,Nt+1))
z_RK45 = sp.zeros((40,Nt+1))

#Condicion inciial en t = 0, i = 0. 
z0 = sp.zeros((40))

z_euler[:,0] = z0
z_RK45[:,0] = z0

print "Integrando con Euler"
fun.tnextreport = 0
fun.solver = "Euler"
   
i = 1
ti = dt 
while (ti < tmax):
    z_euler[:,i] = dt * fun(ti, z_euler[:,i-1]) + z_euler[:,i-1]
    ti += dt
    i += 1

print "Integrando con RK45"
fun.tnextreport = 0
fun.solver = "RK45"
solucion_rk45 = solve_ivp(fun, [0., tmax], z0, method=fun.solver, t_eval=t, vectorized=False)
z_RK45[:,1:] = solucion_rk45.y

   ###########################################################################
# GRÁFICOS
# Gráficos para ambos métodos
for z, lab in zip([z_euler, z_RK45], ["Euler", "RK45"]):

    u = z[0,:]
    v = z[1,:]

    #Extraer desplazamientos y velocidades
    u = z[0,:-1]
    v = z[1,:-1]
    dmax=max(abs(u))
    plt.subplot(3,1,1)
    plt.plot(t, u, label=lab)
    plt.ylim([-1.5*dmax, 1.5*dmax])
    plt.xlim([0, tmax])
    plt.ylabel("Desplazamiento, $u = z_1$ (m)")
    plt.grid(True)

    vmax = max(abs(v))
    plt.subplot(3,1,2)
    plt.plot(t, v)
    plt.ylabel("Velocidad, $\dot{u} = z_2$ (m/s)")
    plt.xlabel("Tiempo, $t$ (s)")
    plt.ylim([-1.5*vmax, 1.5*vmax])
    plt.xlim([0, tmax])
    plt.grid(True)

    plt.subplot(3,1,3)
    tt=sp.arange(0,tmax/1.1)
    plt.plot(tt,f0(tt))
    plt.xlim(0,tmax)
    plt.grid(True)
    plt.ylabel("Registro Sismico ('%'g)")

plt.subplot(3,1,1)
plt.legend()
plt.suptitle("Solucion por metodo de Euler")

plt.show()
