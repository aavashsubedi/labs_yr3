import numpy 
import math

"""
## This python code is based on the MatLab code orginaly provided by Chris Westbrook
## http://www.met.reading.ac.uk/~sws04cdw/viscosity_calc.html

__author__  = "Matthew Partridge"
__license__ = "GPL"
__version__ = "1.0"
__credits__ = "Chris Westbrook"

"""


def glycerine_calc(water_vol, glycerol_vol):
    T = 20 				#temperature (degrees Celcius)
    waterVol = water_vol	#volume of water required (ml)
    glycerolVol = glycerol_vol	#volume of Glycerol used (ml)


    #Densities ----------------

    glycerolDen = (1273.3-0.6121*T)/1000 			#Density of Glycerol (g/cm3)
    waterDen = (1-math.pow(((abs(T-4))/622),1.7)) 	#Density of water (g/cm3)


    #Fraction cacluator ----------------

    glycerolMass=glycerolDen*glycerolVol
    waterMass=waterDen*waterVol
    totalMass=glycerolMass+waterMass
    mass_fraction=glycerolMass/totalMass
    vol_fraction= glycerolVol/(glycerolVol+waterVol)


    ##Andreas Volk polynomial method
    contraction_av = 1-math.pow(3.520E-8*((mass_fraction*100)),3)+math.pow(1.027E-6*((mass_fraction*100)),2)+2.5E-4*(mass_fraction*100)-1.691E-4
    contraction = 1+contraction_av/100

    ## Distorted sine approximation method
    #contraction_pc = 1.1*math.pow(math.sin(numpy.radians(math.pow(mass_fraction,1.3)*180)),0.85)
    #contraction = 1 + contraction_pc/100

    density_mix=(glycerolDen*vol_fraction+waterDen*(1-vol_fraction))*contraction
        
    #    print ("Density of mixture =",round(density_mix,5),"g/cm3")


    #Viscosity calcualtor ----------------

    glycerolVisc=0.001*12100*numpy.exp((-1233+T)*T/(9900+70*T))
    waterVisc=0.001*1.790*numpy.exp((-1230-T)*T/(36100+360*T))

    a=0.705-0.0017*T
    b=(4.9+0.036*T)*numpy.power(a,2.5)
    alpha=1-mass_fraction+(a*b*mass_fraction*(1-mass_fraction))/(a*mass_fraction+b*(1-mass_fraction))
    A=numpy.log(waterVisc/glycerolVisc)

    viscosity_mix=glycerolVisc*numpy.exp(A*alpha)

    #print ("Viscosity of mxiture =",round(viscosity_mix,5), "Ns/m2")
    return viscosity_mix



if __name__=="__main__":
    glycerine_calc(water_vol, glycerol_vol)