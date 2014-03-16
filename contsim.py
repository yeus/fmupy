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
FMUInterface.FMUInterface("./modelicatests_efunc.fmu")


#initialisation:
x0 = self.interface.fmiGetContinuousStates()

#simulation loop:

