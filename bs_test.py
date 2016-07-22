#!/usr/bin/python
# -*- coding: utf-8 -*-

from fmusim import *
import matplotlib.pyplot as plt
import scipy
from scipy.integrate import ode
from math import sin

inputfunctions = {}
varnames = []
#myfmu = fmu("./FMU/om/buildingblocks_verosim_basic.fmu", logging=False) #turn logging off for faster calculation
#myfmu = fmu("./efunc.fmu", logging=False) #turn logging off for faster calculation
myfmu = fmu("./buildingblocks_verosim_basic.fmu", logging = True) #satcomponents_blocks_noise_sampled
 #satcomponents_blocks_noise_sampled#buildingblocks_verosim_basic
contvars=list(myfmu.getContinuousVariables().values())
#statenames=list(myfmu.getStateNames().values())
allvariables = list(myfmu.getVariables().values())

#varnames = ['imu_simple1.y.[1]']#contvars#['imu.y.[1]','imu.y.[2]','imu.y.[3]']
#varnames = ['imu_simple1.y.[1]']#contvars#['imu.y.[1]','imu.y.[2]','imu.y.[3]']
inputfunctions = {'rw_torque': lambda t: 5*sin(t)}
varnames = ['torque','reactionwheelsimple_noelectricity1.torque2.tau','reactionwheelsimple_noelectricity1.limiter1.y']#'reactionwheelsimple_noelectricity1.ctrl_torque','rw_torque','imu1.y.[3]',#['variableresistor1.LossPower','trapezoid1.y']#['imu.y.[1]','imu.y.[2]','imu.y.[3]']
print(allvariables, myfmu.getInputVariables())

dt=0.01
#y0, status, eventInfo = myfmu.initialize(0.0)
#simulation with generic solvers
t_end = 10.0
res = myfmu.simulate(dt=dt, t_end=t_end, varnames = varnames, inputfs = inputfunctions)

#if statenames != []: states = True
#else: states = False

#f = myfmu.f #load right-hand-side functio of ode of the FMU

#print(myfmu.getStateNames())
#res = [[myfmu.getValue(varname) for varname in varnames]]

#file = open("tmp", "w+")

####################################
##start scipy integration

##initialize scipy ode solver
#r = ode(f).set_integrator('dopri5') #more methods: http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.ode.html#scipy.integrate.ode
#r.set_initial_value(y0, t0)
#t , y = [t0],[y0] 
#res = [[myfmu.getValue(varname) for varname in varnames]]
#for tn in np.arange(t0,t1+dt,dt):
    #if states: r.integrate(tn)
    #y += [r.y]
    #t += [r.t]
    ##if not r.successful(): break
    #myfmu.fmiCompletedIntegratorStep()
    #res += [[myfmu.getValue(varname) for varname in varnames]]
    ##print(res)

#####################################
##plot result

def plot(y,t, varnames):
  #print(y)
  #plot only specific variables
  for val, var in zip(y.T,varnames): 
    #if any(val): 
    #check if variables are constant or not
    #if  val.min() != val.max():  #val.max()-val.min() < epsilon  #(a == a[0]).all()
      #print(var, val)
    plt.plot(t,val,label=var[1:] if var[0] == '_' else var )
    
  plt.legend()

y = res[:,1:]
t = res[:,0]
plot(y, t, varnames)

plt.show()