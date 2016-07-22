#!/usr/bin/python
# -*- coding: utf-8 -*-

from fmusim import *
import matplotlib.pyplot as plt
import scipy
from scipy.integrate import ode

#myfmu = fmu("./FMU/om/buildingblocks_verosim_basic.fmu", logging=False) #turn logging off for faster calculation
#myfmu = fmu("./FMU/om/satcomponents_blocks_noisetest.fmu", logging=False) #turn logging off for faster calculation
myfmu = fmu("./ibossmo_components_Examples_interfacecomplete_with_dcdc.fmu", logging=False) #turn logging off for faster calculation
contvars=list(myfmu.getContinuousVariables().values())
statenames=list(myfmu.getStateNames().values())

#print(contvars, statenames)

if statenames != []: states = True
else: states = False

varnames = contvars#['imu.y.[1]','imu.y.[2]','imu.y.[3]']

f = myfmu.f #load right-hand-side functio of ode of the FMU
t0,t1 = 0.0,10.0
dt=1.0
y0, status, eventInfo = myfmu.initialize(0.0)

print(myfmu.getStateNames())
res = [[myfmu.getValue(varname) for varname in varnames]]

#file = open("tmp", "w+")

####################################
##start scipy integration

#initialize scipy ode solver
r = ode(f).set_integrator('dopri5') #more methods: http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.ode.html#scipy.integrate.ode
r.set_initial_value(y0, t0)
t , y = [t0],[y0] 
res = [[myfmu.getValue(varname) for varname in varnames]]
for tn in np.arange(t0,t1+dt,dt):
    if states: r.integrate(tn)
    y += [r.y]
    t += [r.t]
    #if not r.successful(): break
    myfmu.fmiCompletedIntegratorStep()
    res += [[myfmu.getValue(varname) for varname in varnames]]
    print(res)

#####################################
##plot result
y = np.array(y)
res = np.array(res)
def plot():
  #plot state variables
  #for i in y:
    #plt.plot(t,y)
  
  #plot only specific variables
  for y, var in zip(res.T,varnames):
    plt.plot(t,y,label=var.replace('_',''))
    
  plt.legend()
  plt.show()
  
plot()
