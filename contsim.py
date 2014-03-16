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

import time


class fmu(FMUInterface.FMUInterface):
  def __init__(self):
    #keine co-simulation
    super().__init__("./efunc.fmu",loggingOn=False) #init fmu interface
    
    self.changedStartValue={}
    
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


myfmu = fmu()
myfmu.changedStartValue["x"]=3.0

myfmu.fmiSetTime(0.0)

myfmu.initialize(0.0)

dt = 0.01
for t in np.arange(0.0,1.0,dt):
  x  = myfmu.fmiGetContinuousStates()
  dx = myfmu.fmiGetDerivatives()
  
  xn = x + dx*dt
  
  myfmu.fmiSetTime(t)
  
  myfmu.fmiSetContinuousStates(xn)
  
  myfmu.fmiCompletedIntegratorStep()
  
  print(t,x,dx)
  time.sleep(dt)
  

myfmu.fmiTerminate()
myfmu.free()
#initialisation:
#print(interface.description.numberOfContinuousStates)
#.fmiSetContinuousStates(cs)
#x0 = interface.fmiGetContinuousStates()

#print(interface.description.description)
#print(x0)
#print(interface.fmiGetModelTypesPlatform())
#print(interface.fmiGetVersion())
#simulation loop:

