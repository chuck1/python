#!/usr/bin/env python3
"""
Created on Fri Mar 10 16:17:19 2017

@author: msimones

Based on AHRI410 Form 410-5: Rating calculation procedure for sensible air, single phase coils
"""
from __future__ import division
from numpy import cosh, exp, floor, log, pi, sinh, sqrt
from scipy.special import kv, iv #modified Bessel functions (1st and 2nd kind)
import psychro as psy
import fluidProp as fprop

def get_RaD(D_8ths, fpi, Va):
    if D_8ths == 4:
        return 0.2*(fpi/6)**-0.15*(Va/100)**-0.56; #air film thermal resitance for dry surface [h ft^2 degF/Btu]
    elif D_8ths == 5:
        return 0.195*(fpi/8)**(-0.1)*(Va/100)**(-0.605*(fpi/8)**0.052);

def j_w(L,D,Re): # j-factor for single phase fluids, smooth pipe flow = (h/(cp G))*Pr^(2/3)*(mus/mu)^0.14
    #see McAdams, 1942. Heat Transmission, p.196, Fig. 92.
    if Re <= 2100:
        #Re = 2100 per suggestion of Buzz Meyers; 
        res=1.86*(D/L)**(1./3.)*(Re)**(-2./3.);
    elif Re > 2100:
        res=0.027*(Re)**-0.2;     
    return res

if __name__=='__main__':
    
    #Technically should include a correction factor (1+W) for moist air capacity calculations
    #need to include interation step to determine average fluid properties
    #3/30/2017: does not agree with TEMTROL dll, TEMTROL rates higher capacity
    
    #---Inputs---
    H = 30.; #coil finned height [in.]
    L = 60.; #coil finned length [in.]
    Nr = 6; #coil depth in rows
    serp = 1;
    D_8ths = 5; #tube nominal OD in 8ths (3/8 = 3, 1/2 = 4, 5/8 = 5)
    fpi = 8; #fins per inch [fins/in.]
    Yf = 0.008; #fin thickness [in.]
    SCFM =6000; #std. volumetric flow rate [ft^3/min]
    EDB = 80; #entering dry-bulb temp. [degF]
    EWB = 65; #entering wet-bulb temp. [degF]
    GPM = 50; #water flow rate [gpm]
    EWT = 65; #entering water temperature [degF]
    z = 0; #elevation [ft]
    Pbaro = psy.stdAtm(z); #14.696; #ps#barometric pressure [psia]
    kf = 128.3; #fin material thermal conductivity [Btu ft/(h ft^2 degF)]; aluminum = 128.3; copper = 226
    
    #---Coil Geometry---
    if (D_8ths == 3):
        Do = 0.397; #tube outside diameter [in.] ***confirm
        Di = 0.0375; #tube inside diameter [in.] ***confirm
        srow = 0.866; #row spacing [in.] ***confirm
        stube = 1.0; #tube spacing [in.] ***confirm
        Kb = 15.; #equivalent length of coil circuit per return bend [in.] ***confirm
    elif (D_8ths == 4):
        Do = 0.522 #***confirm
        Di = 0.45; #***confirm
        srow = 1.0825; #***confirm
        stube = 1.25; #***confirm
        Kb = 15.; #equivalent length of coil circuit per return bend [in.] ***confirm
    elif (D_8ths == 5):
        Do = 0.647; #***confirm
        Di = 0.575; #***confirm
        srow = 1.299; #***confirm
        stube = 1.5; #***confirm
        Kb = 15.; #equivalent length of coil circuit per return bend [in.] ***confirm
    
    #---Thermophysical Properties
    kt = 226.; #tube thermal conductivity (copper) [Btu ft/(h ft^2 degF)]
    
    cpa = psy.psychro(EDB,Pbaro,'Twb',EWB,'cp'); #specific heat of moist air [Btu/(lbm,da degF)]
    
    rhow = fprop.rhosat_T(EWT,0,'water'); #density of water at entering temp. [lbm/ft^3] ***approx., need to iterate solution
    cpw = fprop.rhosat_T(EWT,0,'water'); #specific heat capacity of water at entering temp. [Btu/(lbm degF)] ***approx., need to iterate solution
    muw = fprop.musat_T(EWT,0,'water'); #viscosity of water at entering temp. [lbm/(ft*hr)] ***approx., need to iterate solution
    kw = fprop.ksat_T(EWT,0,'water'); #thermal conductivity of water at entering temp. [Btu/(hr ft degF)] ***approx., need to iterate solution
    muws = fprop.musat_T(EDB,0,'water'); #viscosity of water at tube surface temp. [lbm/(ft*hr)] ***approx., need to iterate solution
    
    
    #---Calculations
    Lc = 1/fpi; #fin pitch [in.]
    Ld = srow*Nr; #fin depth in direction of airflow [in.]; NOTE: may use the pre-configured depth (depth before sheet metal forming, i.e. total surface depth)
    Lf = H; #fin length (perpendicular to direction of tubes) [in.]; NOTE: may use the pre-configured length (length before sheet metal forming, i.e. total surface length)
    Lt = L; #finned tube length [in.]
    Ls = L; #straight tube length per tube pass [in.] ***confirm
    Nf = fpi*Lf; #Total number for fins
    Ntr = floor(H/stube); #number of tubes in each coil row
    Nt = Ntr*Nr
    Nh = Nt; #total number of holes in fin ***confirm manufacturing practice at punch press
    Nc = serp*Ntr; #number of tube circuits in coil ***confirm
    Af = H*L/144.; #coil face area [ft^2]
    As = Nf*(2*Lf*Ld/144.-2*pi*Nh*(Do+2*Yf)**2/(4.*144)+pi*(Do+2*Yf)*(Nh-Nt)*Lc/144.); #secondary surface area (continuous plate fin) [ft^2]
    Ap = pi*Nt*(Do*Lt-Nf*Yf*(Do-2.*Lc))/144.
    Ao = As + Ap;
    Ai = pi*Di*Nt*Lt/144.; #total internal coil surface area [ft^2]
    Aix = pi*(Di/12)**2*Nc/4.; #total cross-sectional fluid flow area, inside tubes [ft^2]
    B = Ao/Ai; #surface ratio [-]
    Le = (Nr*(Ls + Kb)*(Ntr/Nc)-Kb)/12.; #total equivalent length of coil circuit [ft]
    Va = SCFM/Af; #std. air face velocity [std. ft/min]
    ww = rhow*GPM*(1/7.4805)*(60); #mass flow rate of water [lbm/hr] ***density a function of average water temp., need loop for thermal properties?
    Vw = ww/(62.361*Aix*3600); #ave. std. water velocity [ft/s]
    
    RaD = get_RaD(D_8ths,fpi,Va)
    
    fa = 1/RaD; #air-side film coefficient (faD or faW) [Btu/(h ft^2 degF)]; faD = 1/Rad, faW = (1/RaW)(m"/cp)
    #---Fin Efficiency (Gardner, 1945; summarized in AHRI 410)---
    xe = sqrt(Lf*Ld/(pi*Nt)); #outside radius of equiv. annular area of non-circular fin [in.]
    xb = (Do + 2.*Yf)/2.0; #fin root radius [in.]
    w = xe - xb; #height of equivalent actual annualr fin [in.]
    Ub = w*sqrt(fa/(6*kf*Yf))/(xe/xb-1);
    Ue = Ub*(xe/xb);
    beta1 = iv(1,Ue)/kv(1,Ue)
    phi = (2./(Ub*(1-(Ue/Ub)**2)))*(iv(1,Ub)-beta1*kv(1,Ub))/(iv(0,Ub)+beta1*kv(0,Ub));
    eta = (phi*As+Ap)/Ao; #total external surface effectiveness [-]
    print ("eta",eta)
    Rffa = 0; #tube-side fouling factor
    G = ww/Aix; #mass velocity [Btu/(h ft^2 degF)]
    Prw = (cpw*muw/kw); #Prandtl number [-]
    Rew = Di*G/muw; #Reynolds number of water [-]
    jw = j_w(Ls,Di,Rew); #j-factor for water flow in smooth pipe [-]
    fL = jw*cpw*G*Prw**(-2/3)*(muw/muws)**0.14; #tube-side heat transfer coeff. [Btu/(h ft^2 degF)]
    RL = B*(1/fL+Rffa); #tube-side thermal resistance [(h ft^2 degF)/Btu]
    
    Rt = (B*Di/(2.*kt))*(1./12.)*log(Do/Di); #tube metal thermal resistance [(h ft^2 degF)/Btu]
    R = RaD/eta+Rt+RL; #overall thermal resistance between air and tube-side fluid [(h ft^2 degF)/Btu]
    
    Cair = (0.075*SCFM*cpa*60);
    Cwater = (cpw*ww);
    if Cair <= Cwater:
        Cr = Cair/Cwater; #heat capacity rate ratio Cmin/Cmax [-], Cmin=Cair
        Ntu = (Ao/R)/Cair; #number of transfer units [-], Ntu = UA/Cmin
    else:
        Cr = Cwater/Cair; #heat capacity rate ratio Cmin/Cmax [-], Cmin=Cwater
        Ntu = (Ao/R)/Cwater; #number of transfer units [-], Ntu = UA/Cmin
    
    print("Ntu", Ntu)
    if (Nr == 1): #1-row, air-side unmixed, tube-side mixed
        eff = (1-exp(-Cr*(1-exp(-Ntu))))/Cr;
    elif (Nr == 2): #2- row coil, air-side unmixed, tube-side mixed
        eff = (1-exp(-Cr*(1-exp(-Ntu/2.)))/(cosh(Cr*(1-exp(-Ntu/2)))+exp(-Ntu/2)*sinh(Cr*(1-exp(-Ntu/2)))))/Cr;
    elif (Nr >= 3): #3+ row, thermal counterflow
        if (Cr == 1):
            eff = Ntu/(Ntu+1);
        else:
            eff = (1-exp(-Ntu*(1-Cr)))/(1-Cr*exp(-Ntu*(1-Cr)));
    print("eff",eff)
    if (EWT > EDB): #air-heating coil
        deltaT0 = EWT - EDB; #maximum temperature difference [degF]
        qs = eff*(0.075*60*SCFM*cpa*deltaT0); #sensible heating capacity [Btu/hr]
        deltaTa = qs/(0.075*60*cpa*SCFM); #air-side temperature difference [degF]
        LDB = EDB + deltaTa #leaving dry-bulb temperature [degF]
        deltaTw = qs/(ww*cpw); #tube-side temperature difference [degF]
        LWT = EWT- deltaTw; #leaving water temperature [degF]
        Twave = (EWT+LWT)/2.;
    elif (EWT < EDB): #air-cooling coil
        deltaT0 = EDB - EWT; #maximum temperature difference [degF]
        qs = eff*(0.075*60*SCFM*cpa*deltaT0); #sensible cooling capacity [Btu/hr]
        deltaTa = qs/(0.075*60*cpa*SCFM); #air-side temperature difference [degF]
        LDB = EDB - deltaTa; #leaving dry-bulb temperature [degF]
        deltaTw = qs/(ww*cpw); #tube-side temperature difference [degF]
        LWT = EWT + deltaTw; #leaving water temperature [degF]
        Twave = (EWT+LWT)/2.;
    
    print ("qs",qs)
    print ("LDB",LDB)
    print ("LWT",LWT)
