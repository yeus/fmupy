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
import fmusim2
from scipy import interpolate

##myfmu = fmu("./Modelica_Mechanics_MultiBody_Examples_Elementary_DoublePendulum.fmu")
##myfmu = fmu("./Modelica_Mechanics_MultiBody_Examples_Elementary_Pendulum.fmu")
##myfmu = fmu("./FMU/Batteriebaustein.fmu")
##myfmu = fmu("./Modelica_Mechanics_Rotational_Examples_First.fmu")
#myfmu = fmu("./efunc.fmu")
#myfmu = fmu("satcomponents_blocks_noise_sampled.fmu", logging = False)
#myfmu = fmu("rosmo_ExternalLibraries.fmu", logging = True)
#myfmu = fmusim.fmu("FMU/iboss_vti.fmu", logging = True)
#with fmusim2.fmi("./FMU/efunc.fmu", loggingOn = True) as myfmu:
myfmu = fmusim2.fmi("./fmu/satcomponents_AOCS_examples_mission_simulation_ideal.fmu", loggingOn = False)
##myfmu.printvarprops()
##print(myfmu.getOutputNames())
#names=list(myfmu.getOutputNames().values())
#names=myfmu.getStateNames()
#names = myfmu.getVariables()
#print(names)
#names=[#'iXp.comm_out.tmp','iXp.comm_out.mi_pos',"set_mi_pos.[1]"]
names = ['body1.r_0[1]']

def intpl1d(table):
    table = np.array(table)
    return interpolate.interp1d(table[:,0],table[:,1], kind = 0)#‘linear’, ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic, ‘cubic’ where ‘slinear’, ‘quadratic’ and ‘cubic’ 

#simulation with generic solvers
t_end = 10.0
#ctrlmi = intpl1d([[0.0,0.0],[10.0,0.5],[20.0,0.1],[150.0,0.9],[1000000.0,1.0]])
#infuncs = {'set_mi_pos.[1]':ctrlmi}
#res = myfmu.simulate(dt=10.0, t_end=t_end, varnames = names, inputfs = infuncs)
res = myfmu.simulate(dt=.001, t_end=t_end, varnames = names)

import matplotlib.pyplot as plt
def plot():
  for name in res.dtype.names[1:]:
    plt.plot(res.t,res[name],label=name)
    
  plt.legend()
  plt.show()
  
plot()

myfmu.free()

