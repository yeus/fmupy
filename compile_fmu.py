#!/home/tom/build/jmodelica/bin/jm_python.sh
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

#clean modelica files from annotations:  annotation\(([^;]|[^\)].|\n)*[\);]+

# Import the compiler function
from pymodelica import compile_fmu

#Specify Modelica model and model file (.mo or .mop)
#mo_file = '../../../model/satcomponents/modelicatests.mo' #satcomponents #buildingblocks
#model_name = 'modelicatests.constraints_test' #noisetest #sample_test #satcomponents.blocks.noise_sampled
#mo_file = '../../../model/satcomponents/buildingblocks.mo'
#model_name = 'buildingblocks.verosim_basic'
#mo_file = '../model/satcomponents/ibossmo.mo'
#model_name = 'ibossmo.buildingblocks.verosim_basic'
#model_name = 'ibossmo.buildingblocks.examples.verosim_block'
#model_name = 'ibossmo.components.Examples.interfacecomplete_with_dcdc'
mo_file = '/home/tom/iboss_sim/model/satcomponents/satcomponents.mo'
model_name = 'satcomponents.AOCS.examples.mission_simulation_ideal'
#mo_file = "efunc.mo"
#model_name = 'efunc'



# Compile the model and save the return argument, which is the file name of the FMU
#my_fmu = compile_fmu(model_name,mo_file, target='me',compiler_options = {'extra_lib_dirs':'../../../model/satcomponents'}, version = '1.0')
my_fmu = compile_fmu(model_name, mo_file, target='cs',compiler_options = {'extra_lib_dirs':'../model/satcomponents'}, version = '2.0')  #target='cs'  for cosimulation, otherwise, just for model exchange
#my_fmu = compile_fmu(model_name, mo_file, target='cs', version = '2.0')  #target='cs'  for cosimulation, otherwise, just for model exchange

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

