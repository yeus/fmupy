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


# Import the compiler function
from pymodelica import compile_fmu

#Specify Modelica model and model file (.mo or .mop)
mo_file = '../../../model/satcomponents/satcomponents.mo'
model_name = 'satcomponents.blocks.sample_test' #noisetest
#mo_file = '../../../model/satcomponents/buildingblocks.mo'
#model_name = 'buildingblocks.verosim_basic'


# Compile the model and save the return argument, which is the file name of the FMU
#my_fmu = compile_fmu(model_name,mo_file, target='me',compiler_options = {'extra_lib_dirs':'../../../model/satcomponents'})
my_fmu = compile_fmu(model_name, mo_file, target='cs',compiler_options = {'extra_lib_dirs':'../../../model/satcomponents'})  #target='cs'  for cosimulation, otherwise, just for model exchange

# Compile an example model from the MSL
#fmu1 = compile_fmu('Modelica.Mechanics.Rotational.Examples.First')

## Compile a model from the library MyLibrary, located in C:\MyLibs
#fmu2 = compile_fmu('MyLibrary.MyModel', compiler_options = {'extra_lib_dirs':'C:\MyLibs'})

## The same as the last command, if no other libraries in C:\MyLibs are needed
#fmu3 = compile_fmu('MyLibrary.MyModel', 'C:\MyLibs\MyLibrary')


#JMUs:
## Import the compiler function
#from pymodelica import compile_jmu

## Specify Modelica or Optimica model and model file (.mo or .mop)
#model_name = 'myPackage.myModel'
#mo_file = 'myModelFile.mo'

## Compile the model and save the return argument, which is the file name of the FMU
#my_jmu = compile_jmu(model_name, mo_file)

