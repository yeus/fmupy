#myfmu = fmu("./FMU/Batteriebaustein.fmu")
myfmu = fmu("./efunc.fmu")
#res=myfmu.cosimulate()

#myfmu = fmu("./Modelica_Mechanics_Rotational_Examples_First.fmu")
#myfmu.printvarprops()
#print(myfmu.getOutputNames())
names=list(myfmu.getContinuousVariables().values())
#names=myfmu.getStateNames()


import scipy
from scipy.integrate import ode

f = myfmu.f #loaded FMU
t0 = 0.0
y0, status, eventInfo = myfmu.initialize(0.0)

r = ode(f).set_integrator('zvode', method='bdf')
r.set_initial_value(y0, t0)
t1 = 10
dt = 1
while r.successful() and r.t < t1:
    r.integrate(r.t+dt)
    print("{}  {}".format(r.t, r.y))


#t_end = 10.0
#res = myfmu.simulate(dt=1.0, t_end=t_end,varnames=names)


#import matplotlib.pyplot as plt


#x = np.linspace(0.0,t_end,100.0)
#plt.plot(x,np.exp(x))
#def plot():
  #for i,vals in enumerate(res[:,1:].T):
    #plt.plot(res[:,0],vals,label=names[i])
    
  #plt.legend()
  #plt.show()
  
#plot()

##myfmu.plot(res[])

##numpy.savetxt("foo.csv", a, delimiter=",")

##myfmu.changedStartValue["x"]=3.0

##myfmu.fmiTerminate()
##myfmu.free()


#initialisation:
#print(interface.description.numberOfContinuousStates)
#.fmiSetContinuousStates(cs)
#x0 = interface.fmiGetContinuousStates()

#print(interface.description.description)
#print(x0)
#print(interface.fmiGetModelTypesPlatform())
#print(interface.fmiGetVersion())
#simulation loop: