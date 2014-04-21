#!/usr/bin/python
# -*- coding: utf-8 -*-


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

import FMUInterface
from FMUInterface import fmiTrue, fmiFalse

from operator import itemgetter

import time

import types


class fmu(FMUInterface.FMUInterface):
  def __init__(self, file):
    super(fmu, self).__init__(file,loggingOn=True) #init fmu interface
    
    self.changedStartValue={}

#  def getStateNames(self):
#      ''' Returns a list of Strings: the names of all states in the model.
#      '''
#      references = self.fmiGetStateValueReferences()
#      allVars = list(self.description.scalarVariables.items())
#      referenceListSorted = [(index, var[1].valueReference) for index, var in enumerate(allVars)]
#      referenceListSorted.sort(key=itemgetter(1))
#      referenceList = [r[1] for r in referenceListSorted]
#
#      names = []
#      for ref in references:
#          if ref == -1:
#              # No reference available -> name is hidden
#              names.append('')
#          else:
#              k = referenceList.count(ref)
#              if k > 0:
#                  index = -1
#                  i = 0
#                  while i < k:
#                      i += 1
#                      index = referenceList.index(ref, index + 1)
#                      if allVars[referenceListSorted[index][0]][1].alias is None:
#                          name = allVars[referenceListSorted[index][0]][0]
#                          names.append(name)
#                          break
#              else:
#                  # Reference not found. Should not occur.
#                  names.append('')
#      return names

  def getValue(self, name):
      ''' Returns the values of the variables given in name;
          name is either a String or a list of Strings.            
      '''
      if type(name) == list:
          n = len(name)
          nameList = True
          names = name
      else:
          n = 1
          nameList = False
          names = [name]

      iReal = []
      iInteger = []
      iBoolean = []
      iString = []
      refReal = []
      refInteger = []
      refBoolean = []
      refString = []
      for i, x in enumerate(names):
          dataType = self.description.scalarVariables[x].type.type
          if dataType == 'Real':
              refReal.append(self.description.scalarVariables[x].valueReference)
              iReal.append(i)
          elif dataType == 'Integer':
              refInteger.append(self.description.scalarVariables[x].valueReference)
              iInteger.append(i)
          elif dataType == 'Boolean':
              refBoolean.append(self.description.scalarVariables[x].valueReference)
              iBoolean.append(i)
          elif dataType == 'String':
              refString.append(self.description.scalarVariables[x].valueReference)
              iString.append(i)

      #TODO: hier werden Werte für bestimmte Variablen abgerufen.
      retValue = list(range(n))
      k = len(refReal)
      if k > 0:
          ref = FMUInterface.createfmiReferenceVector(k)
          for i in range(k):
              ref[i] = refReal[i]
          values = self.fmiGetReal(ref)
          for i in range(k):
              retValue[iReal[i]] = values[i]
      k = len(refInteger)
      if k > 0:
          ref = FMUInterface.createfmiReferenceVector(k)
          for i in range(k):
              ref[i] = refInteger[i]
          values = self.fmiGetInteger(ref)
          for i in range(k):
              retValue[iInteger[i]] = values[i]
      k = len(refBoolean)
      if k > 0:
          ref = FMUInterface.createfmiReferenceVector(k)
          for i in range(k):
              ref[i] = refBoolean[i]
          values = self.fmiGetBoolean(ref)
          for i in range(k):
              retValue[iBoolean[i]] = values[i]
      k = len(refString)
      if k > 0:
          ref = FMUInterface.createfmiReferenceVector(k)
          for i in range(k):
              ref[i] = refString[i]
          values = self.fmiGetString(ref)
          for i in range(k):
              retValue[iString[i]] = values[i]

      if nameList:
          return retValue
      else:
          return retValue[0]
    
  def setValue(self, valueName, valueValue):
      ''' set the variable valueName to valueValue
          @param valueName: name of variable to be set
          @type valueName: string
          @param valueValue: new value
          @type valueValue: any type castable to the type of the variable valueName
      '''
      ScalarVariableReferenceVector = FMUInterface.createfmiReferenceVector(1)
      ScalarVariableReferenceVector[0] = self.description.scalarVariables[valueName].valueReference
      if self.description.scalarVariables[valueName].type.type == 'Real':
          ScalarVariableValueVector = FMUInterface.createfmiRealVector(1)
          ScalarVariableValueVector[0] = float(valueValue)
          self.fmiSetReal(ScalarVariableReferenceVector, ScalarVariableValueVector)
      elif self.description.scalarVariables[valueName].type.type in ['Integer', 'Enumeration']:
          ScalarVariableValueVector = FMUInterface.createfmiIntegerVector(1)
          ScalarVariableValueVector[0] = int(valueValue)
          self.fmiSetInteger(ScalarVariableReferenceVector, ScalarVariableValueVector)
      elif self.description.scalarVariables[valueName].type.type == 'Boolean':
          ScalarVariableValueVector = FMUInterface.createfmiBooleanVector(1)
          if valueValue == "true":
              ScalarVariableValueVector[0] = fmiTrue
          else:
              ScalarVariableValueVector[0] = fmiFalse
          self.fmiSetBoolean(ScalarVariableReferenceVector, ScalarVariableValueVector)
      elif self.description.scalarVariables[valueName].type.type == 'String':
          ScalarVariableValueVector = FMUInterface.createfmiStringVector(1)
          ScalarVariableValueVector[0] = str(valueValue)
          self.fmiSetString(ScalarVariableReferenceVector, ScalarVariableValueVector)


  def printvarprops(self):
      ''' Returns a list of Strings: the names of all output variables in the model.
      '''
      names = {}
      for key,var in self.description.scalarVariables.items():
          #if var.causality=='output':
            print("{:<40}{v.valueReference:<30}{v.alias:<20}{v.variability}".format(key,v=var))#key, var.valueReference, var.alias, var.variability, var.description, var.causality,var.directDependency,  var.type)
            #if key[0]=='_': key=key[1:]  #matplotlib labels don#t recognize '_'
            #names[var.valueReference]=key
              
      return names      

  def getContinuousVariables(self):
      if self._mode is 'me':
        return self.getVariables('continuous')
      elif self._mode is 'cs':
        return self.getVariables('continuous')

  def getOutputNames(self):
      ''' Returns a list of Strings: the names of all output variables in the model.
      '''
      names = {}
      for key,var in self.description.scalarVariables.items():
          if var.causality=='output':
            #print(key, var.valueReference, var.alias, var.variability, var.description, var.causality,var.directDependency,  var.type)
            if key[0]=='_': key=key[1:]  #matplotlib labels don#t recognize '_'
            names[var.valueReference]=key
              
      return names      

  def getStateNames(self):
      ''' Returns a list of Strings: the names of all states in the model.
      '''
      references = self.fmiGetStateValueReferences()

      names = {}
      for key,var in self.description.scalarVariables.items():
          if var.valueReference in references and var.variability=='continuous':
            #print(key, var.valueReference, var.alias, var.variability, var.description, var.causality,var.directDependency,  var.type)
            if key[0]=='_': key=key[1:]  #matplotlib labels don#t recognize '_'
            names[var.valueReference]=key
              
      return names

  def getVariables(self, variability = 'all', causality = 'all'):
      ''' 
	variability:  return variables with variability property
	Returns:  
	  a list of Strings: the namesof the variables with a certain property
      '''

      names = {}
      for key,var in self.description.scalarVariables.items():
          if variability == 'all' or var.variability==variability:
            #print(key, var.valueReference, var.alias, var.variability, var.description, var.causality,var.directDependency,  var.type)
            if key[0]=='_': key=key[1:]  #matplotlib labels don#t recognize '_'
            names[var.valueReference]=key
              
      return names

  def initialize(self, t, errorTolerance=1e-9):
      ''' Initializes the model at time = t with
          changed start values given by the dictionary
          self.changedStartValue.
          The function returns a status flag and the next time event.
      '''
      
      # Terminate last simulation in model
      #self.interface.fmiTerminate()
      #print("Set start time")
      #self.interface.fmiSetTime(t)
      # Set start values
      #self._setDefaultStartValues()
      for name in list(self.changedStartValue.keys()):
          self.setValue(name, self.changedStartValue[name])
      # Initialize model
      eventInfo, status = self.fmiInitialize(fmiTrue, errorTolerance)
      x0 = self.fmiGetContinuousStates()
      return x0, status, eventInfo

  def f(self,t,y):
      """ return a function which can be used for external solver
      
      the example (just small differences, no jacobian) from the scipy intergrator:
      
      http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.ode.html#scipy.integrate.ode
      
      The integration:
         f = myfmu.f #loaded FMU
         t0 = 0.0
         y0 = myfmu.initialize(0.0)

         r = ode(f).set_integrator('zvode', method='bdf')
         r.set_initial_value(y0, t0)
         t1 = 10
         dt = 1
         while r.successful() and r.t < t1:
             r.integrate(r.t+dt)
             print("%g %g" % (r.t, r.y))
      """
      
      self.fmiSetTime(t)
      self.fmiSetContinuousStates(y)
      
      ny = self.fmiGetDerivatives()
      
      return ny

  def simulate(self,dt=0.01, t_start=0.0, t_end=1.0, varnames=[]):
    if self._mode == 'me':
      print("run me-simulation")
      return self.mesimulate(dt, t_start, t_end, varnames)
    elif self._mode == 'cs':
      print("run co-simulation")
      return self.cosimulate(dt, t_start, t_end, varnames)

  def mesimulate(self,dt=0.01, t_start=0.0, t_end=1.0, varnames=[]):
    def RK4(y,t,h,f):
        h05 = h * .5
        t05 = t + h05
        k1=f(t,y);
        k2=f(t05,y+h05*k1);
        k3=f(t05,y+h05*k2);
        k4=f(t+h,y+h*k3);
        yn=y+h/6.0*(k1+2*(k2+k3)+k4)
        return yn

    self.fmiSetTime(0.0)

    x,status,eventInfo = self.initialize(0.0)

    res = [[0.0]+[self.getValue(varname) for varname in varnames]]
    #integration loop
    for t in np.arange(t_start,t_end,dt):
      #x = x + dt * self.f(t,x) #explicit euler
      x = RK4(x,t,dt,self.f) #explicit Runge-Kutta 4 (RK4)
     
      self.fmiCompletedIntegratorStep()
      
      #save results in array
      #print(t,x,dx)
      step=[[t+dt]+[self.getValue(varname) for varname in varnames]]
      if np.nan in step:
        print(step)
        break
      #time.sleep(dt)
      res+=step
      
    
    self.fmiTerminate()
    
    return np.array(res)

  def cosimulate(self, dt=0.01, t_start = 0.0, t_end = 1.0, varnames=[]):
    tc = t_start #current master time
    
    self.fmiInitializeSlave(t_start, True, t_end)
    res=[]
    
    while tc < t_end:
      step=[[tc]+[self.getValue(varname) for varname in varnames]]
      
      self.fmiDoStep(tc, dt, True)
      res+=step
      tc+=dt

    self.fmiTerminateSlave()
    
    return np.array(res)



#myfmu = fmu("./Modelica_Mechanics_MultiBody_Examples_Elementary_DoublePendulum.fmu")
#myfmu = fmu("./Modelica_Mechanics_MultiBody_Examples_Elementary_Pendulum.fmu")

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

