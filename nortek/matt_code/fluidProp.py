# -*- coding: utf-8 -*-
"""
Created on Sat Mar 04 09:07:34 2017

@author: msimones
"""
from __future__ import division
import CoolProp.CoolProp as cprop
"""
Provides fluid property functions for vairous fluids from CoolProp library
separate functions available for saturated or single phase fluids to keep function
inputs to a minimum. 

Provides inputs and outputs in IP units (T= [degF], P= [psia])

rho = [lbm/ft^3]
v = [ft^3/lbm]
h = [Btu/lbm]
cp = [Btu/(lbm degF)]
mu = [lbm/(ft hr)]
k = [Btu/(hr ft degF)]
s = [Btu/(lbm degF)]

Works for: 'water', 'R134a', 'R410a'
NOTE: enthalpy and entropy values depend on reference state. Always compare
enthalpy or entropy differences, not absolute values
"""
#---Properties at saturation---
def satT(P, fluid): #saturation temperature [degF]
    return cprop.PropsSI('T','P',P*(101325/14.696),'Q',0,fluid)*(1.8)-459.67

def satP(T, fluid): #saturation pressure [psia]
    return cprop.PropsSI('P','T',(T+459.67)/1.8,'Q',0,fluid)*(14.696/101325)
        
def rhosat_T(T,X,fluid): #density at saturated temp. and quality [lbm/ft^3]
    return cprop.PropsSI('D','T',(T+459.67)/1.8,'Q',X,fluid)*(1./0.453592)*(1./3.28)**3
    
def rhosat_P(P,X,fluid): #density at saturated pressure and quality [lbm/ft^3]
    return cprop.PropsSI('D','P',P*(101325/14.696),'Q',X,fluid)*(1./0.453592)*(1./3.28)**3
    
def vsat_T(T,X,fluid): #specific volume at saturated temp. and quality [ft^3/lbm]
    return 1/(cprop.PropsSI('D','T',(T+459.67)/1.8,'Q',X,fluid)*(1./0.453592)*(1./3.28)**3)
    
def vsat_P(P,X,fluid): #specific volume at saturated pressure and quality [ft^3/lbm]
    return 1/(cprop.PropsSI('D','P',P*(101325/14.696),'Q',X,fluid)*(1./0.453592)*(1./3.28)**3)
    
def hsat_T(T,X,fluid): #specific enthalpy at saturated temp. and quality [Btu/lbm]
    return cprop.PropsSI('H','T',(T+459.67)/1.8,'Q',X,fluid)*(1/1055.06)*(0.453592/1.)
    
def hsat_P(P,X,fluid): #specific enthalpy at saturated pressure and quality [Btu/lbm]
    return cprop.PropsSI('H','P',P*(101325/14.696),'Q',X,fluid)*(1/1055.06)*(0.453592/1.)
    
def cpsat_T(T,X,fluid): #specific heat capacity at saturated temp. and quality [Btu/(lbm degF)]
    return cprop.PropsSI('CPMASS','T',(T+459.67)/1.8,'Q',X,fluid)*(1/1055.06)*(0.453592/1.)*(1./1.8)
    
def cpsat_P(P,X,fluid): #specific heat capacity at saturated pressure and quality [Btu/(lbm degF)]
    return cprop.PropsSI('CPMASS','P',P*(101325/14.696),'Q',X,fluid)*(1/1055.06)*(0.453592/1.)*(1./1.8)
    
def musat_T(T,X,fluid): #viscosity at saturated temp. and quality [lbm/(ft hr)]
    return cprop.PropsSI('V','T',(T+459.67)/1.8,'Q',X,fluid)*(14.696/101325)*(32.18/1.)*(144/1.)*(3600/1.) #(Pa*sec -> lbm/(ft*hr))
    
def musat_P(P,X,fluid): #viscosity at saturated temp. and quality [lbm/(ft hr)]
    return cprop.PropsSI('V','P',P*(101325/14.696),'Q',X,fluid)*(14.696/101325)*(32.18/1.)*(144/1.)*(3600/1.)
    
def ksat_T(T,X,fluid): #thermal conductivity at saturated temp. and quality [Btu/(hr ft degF)]
    return cprop.PropsSI('CONDUCTIVITY','T',(T+459.67)/1.8,'Q',X,fluid)*(200/3516)*(1/1.8)*(1/3.28)*(60/1.) #W/(m K) -> Btu/(hr ft degR)
    
def ksat_P(P,X,fluid): #thermal conductivity at saturated pressure and quality [Btu/(hr ft degF)]
    return cprop.PropsSI('CONDUCTIVITY','P',P*(101325/14.696),'Q',X,fluid)*(200/3516)*(1/1.8)*(1/3.28)*(60/1.)

def ssat_T(T,X,fluid): #specific entropy at saturated temp. and quality [Btu/(lbm degF)] 
    return cprop.PropsSI('S','T',(T+459.67)/1.8,'Q',X,fluid)*(1/1055.06)*(0.453592/1.)*(1./1.8) #J/(kg K) -> Btu/(lbm degR)
    
def ssat_P(P,X,fluid): #specific entropy at saturated temp. and quality [Btu/(lbm degF)] 
    return cprop.PropsSI('S','P',P*(101325/14.696),'Q',X,fluid)*(1/1055.06)*(0.453592/1.)*(1./1.8) #J/(kg K) -> Btu/(lbm degR)
    
#---sub-cooled and superheated region; **will give errors if evaluated too close to saturation line---
def rho_PT(P,T,fluid): #density at pressure and temp. [lbm/ft^3]
    return cprop.PropsSI('D','P',P*(101325/14.696),'T',(T+459.67)/1.8,fluid)*(1./0.453592)*(1./3.28)**3
    
def v_PT(P,T,fluid): #specific volume at pressure and temp. [lbm/ft^3]
    return 1/(cprop.PropsSI('D','P',P*(101325/14.696),'T',(T+459.67)/1.8,fluid)*(1./0.453592)*(1./3.28)**3)
    
def h_PT(P,T,fluid): #specific enthalpy at pressure and temp. [Btu/lbm]
    return cprop.PropsSI('H','P',P*(101325/14.696),'T',(T+459.67)/1.8,fluid)*(1/1055.06)*(0.453592/1.) 
     
def cp_PT(P,T,fluid): #specific heat capacity at pressure and temp. [Btu/(lbm degF)]
    return cprop.PropsSI('CPMASS','P',P*(101325/14.696),'T',(T+459.67)/1.8,fluid)*(1/1055.06)*(0.453592/1.)*(1./1.8)
    
def mu_PT(P,T,fluid): #viscosity at pressure and temp. [lbm/(ft hr)]
    return cprop.PropsSI('V','P',P*(101325/14.696),'T',(T+459.67)/1.8,fluid)*(14.696/101325)*(32.18/1.)*(144/1.)*(3600/1.) #(Pa*sec -> lbm/(ft*hr))
    
def k_PT(P,T,fluid): #thermal conductivity at pressure and temp. [Btu/(hr ft degF)]
    return cprop.PropsSI('CONDUCTIVITY','P',P*(101325/14.696),'T',(T+459.67)/1.8,fluid)*(200/3516)*(1/1.8)*(1/3.28)*(60/1.) #W/(m K) -> Btu/(hr ft degR)

def s_PT(P,T,fluid): #specific entropy at pressure and temp. [Btu/(lbm degF)] 
    return cprop.PropsSI('S','P',P*(101325/14.696),'T',(T+459.67)/1.8,fluid)*(1/1055.06)*(0.453592/1.)*(1./1.8) #J/(kg K) -> Btu/(lbm degR)