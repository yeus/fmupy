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
    #keine co-simulation
    super().__init__(file,loggingOn=False) #init fmu interface
    
    self.changedStartValue={}

  def getStateNames(self):
      ''' Returns a list of Strings: the names of all states in the model.
      '''
      references = self.fmiGetStateValueReferences()
      allVars = list(self.description.scalarVariables.items())
      referenceListSorted = [(index, var[1].valueReference) for index, var in enumerate(allVars)]
      referenceListSorted.sort(key=itemgetter(1))
      referenceList = [r[1] for r in referenceListSorted]

      names = []
      for ref in references:
          if ref == -1:
              # No reference available -> name is hidden
              names.append('')
          else:
              k = referenceList.count(ref)
              if k > 0:
                  index = -1
                  i = 0
                  while i < k:
                      i += 1
                      index = referenceList.index(ref, index + 1)
                      if allVars[referenceListSorted[index][0]][1].alias is None:
                          name = allVars[referenceListSorted[index][0]][0]
                          names.append(name)
                          break
              else:
                  # Reference not found. Should not occur.
                  names.append('')
      return names

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

#  def getStateNames(self):
#      ''' Returns a list of Strings: the names of all states in the model.
#      '''
#      references = self.fmiGetStateValueReferences()
#
#      names = {}
#      for key,var in self.description.scalarVariables.items():
#          if var.valueReference in references and var.variability=='continuous':
#            #print(key, var.valueReference, var.alias, var.variability, var.description, var.causality,var.directDependency,  var.type)
#            names[var.valueReference]=key
#              
#      return names

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
      return status, eventInfo

  def simulate(self,dt=0.01, t_start=0.0, t_end=1.0):
    self.fmiSetTime(0.0)

    self.initialize(0.0)

    res=[]

    for t in np.arange(t_start,t_end,dt):
      x  = self.fmiGetContinuousStates()
      dx = self.fmiGetDerivatives()
      
      xn = x + dx*dt
      
      self.fmiSetTime(t)
      
      self.fmiSetContinuousStates(xn)
      
      self.fmiCompletedIntegratorStep()
      
      #print(t,x,dx)
      step=[[t]+list(x)]
      if np.nan in step:
        print(step)
        break
      #time.sleep(dt)
      res+=step
      
    
    self.fmiTerminate()
    
    return np.array(res).T



#myfmu = fmu("./Modelica_Mechanics_MultiBody_Examples_Elementary_DoublePendulum.fmu")
#myfmu = fmu("./Modelica_Mechanics_MultiBody_Examples_Elementary_Pendulum.fmu")

myfmu = fmu("./efunc.fmu")

res=myfmu.simulate(dt=0.01, t_end=300.0)
names=myfmu.getStateNames()

import matplotlib.pyplot as plt
def plot():
  for i,vals in enumerate(res[1:]):
    plt.plot(res[0],vals,label=names[i])
    
  plt.legend()
  plt.show()

#myfmu.plot(res[])

#numpy.savetxt("foo.csv", a, delimiter=",")

#myfmu.changedStartValue["x"]=3.0

#myfmu.fmiTerminate()
#myfmu.free()


#initialisation:
#print(interface.description.numberOfContinuousStates)
#.fmiSetContinuousStates(cs)
#x0 = interface.fmiGetContinuousStates()

#print(interface.description.description)
#print(x0)
#print(interface.fmiGetModelTypesPlatform())
#print(interface.fmiGetVersion())
#simulation loop:

