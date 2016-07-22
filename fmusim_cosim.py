#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
#

# filename: contsim.py
# author: - Thomas Meschede
#
# 
# Test simulation of FMI files using the provided FMI Interface from pysimulator from DLR
#
#
#
# modified:
#       - 2012 11 22 - Thomas Meschede


import numpy as np
import scipy as sp
import fmusim
from scipy import interpolate

##myfmu = fmu("./Modelica_Mechanics_MultiBody_Examples_Elementary_DoublePendulum.fmu")
##myfmu = fmu("./Modelica_Mechanics_MultiBody_Examples_Elementary_Pendulum.fmu")
##myfmu = fmu("./FMU/Batteriebaustein.fmu")
##myfmu = fmu("./Modelica_Mechanics_Rotational_Examples_First.fmu")
#myfmu = fmu("./efunc.fmu")
#myfmu = fmu("satcomponents_blocks_noise_sampled.fmu", logging = False)
#myfmu = fmu("rosmo_ExternalLibraries.fmu", logging = True)
myfmu = fmusim.fmu("iboss_vti.fmu", logging = True)


##myfmu.printvarprops()
##print(myfmu.getOutputNames())
names=list(myfmu.getOutputNames().values())
##names=myfmu.getStateNames()
names=[#'iXp.comm_out.tmp',
        'iXp.comm_out.mi_pos',"set_mi_pos.[1]"]

def intpl1d(table):
    table = np.array(table)
    return interpolate.interp1d(table[:,0],table[:,1], kind = 0)#‘linear’, ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic, ‘cubic’ where ‘slinear’, ‘quadratic’ and ‘cubic’ 

#simulation with generic solvers
t_end = 100.0
ctrlmi = intpl1d([[0.0,0.0],[10.0,0.5],[1000000.0,1.0]])
infuncs = {'set_mi_pos.[1]':ctrlmi}
res = myfmu.simulate(dt=1.0, t_end=t_end, varnames = names, inputfs = infuncs)

import matplotlib.pyplot as plt
def plot():
  for i,vals in enumerate(res[:,1:].T):
    plt.plot(res[:,0],vals,label=names[i])
    
  plt.legend()
  plt.show()
  
plot()


