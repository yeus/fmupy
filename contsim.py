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


import FMUInterface

#keine co-simulation
interface=FMUInterface.FMUInterface("./efunc.fmu")


#initialisation:
x0 = interface.fmiGetContinuousStates()

print(x0)
#simulation loop:

