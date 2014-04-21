#!/usr/bin/python
# -*- coding: utf-8 -*-

from fmusim import *
import matplotlib.pyplot as plt
import scipy
from scipy.integrate import ode

myfmu = fmu("./efunc.fmu")
names=list(myfmu.getContinuousVariables().values())

f = myfmu.f #loaded FMU
t0,t1 = 0.0,10.0
dt=1.0
y0, status, eventInfo = myfmu.initialize(0.0)

#initialize scipy ode solver
r = ode(f).set_integrator('dopri5') #more methods: http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.ode.html#scipy.integrate.ode
r.set_initial_value(y0, t0)
t , y = [t0],[y0] 
for tn in np.arange(t0,t1+dt,dt):
    r.integrate(tn)
    y += [r.y]
    t += [r.t]
    #if not r.successful(): break
    myfmu.fmiCompletedIntegratorStep()

####################################
#plot result
y = np.array(y)
x = np.linspace(0.0,10.0,100.0)
plt.plot(x,np.exp(x))
def plot():
  #plot state variables
  for i in y:
    plt.plot(t,y)
  
  #plot only specific variables
  #for i,vals in enumerate(res[0]):
    #plt.plot(t,y,vals,label=names[i])
    
  plt.legend()
  plt.show()
  
plot()
