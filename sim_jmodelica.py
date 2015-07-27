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
# Import the plotting library
import matplotlib.pyplot as plt

from operator import itemgetter

import time

import types


# Import the compiler function
from pymodelica import compile_fmu
from pyfmi import load_fmu

#Specify Modelica model and model file (.mo or .mop)
mo_file = '../model/satcomponents/satcomponents.mo'
#model_name = 'ibossmo_buildingblocks_examples_verosim_block.fmu' #noisetest
model_name = 'ibossmo_components_Examples_interfacecomplete_with_dcdc.fmu'
#mo_file = '../../../model/satcomponents/buildingblocks.mo'
#model_name = 'buildingblocks.verosim_basic'

model = load_fmu(model_name)

#opts = model.simulate_options()          # Retrieve the default options
#opts['solver'] = 'CVode'                # Not necessary, default solver is CVode
#opts['CVode_options']['discr'] = 'Adams' # Change from using BDF to Adams
#opts['initialize'] = False               # Don't initialize the model
#model.simulate(options=opts)             # Pass in the options to simulate and simulate

#res = model.simulate(final_time=1.0,options=opts)#,algorithm='AssimuloFMIAlg',)
res = model.simulate(final_time=3.0)#,algorithm='AssimuloFMIAlg',)


#plt.plot(res['time'],res['dcpm[1].phiMechanical'])
plt.plot(res['time'],res['timetable1.y'])
plt.show()
