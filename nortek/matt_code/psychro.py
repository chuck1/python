from __future__ import division
import numpy as np

def stdAtm(z,outtype='p'):
    #z = elevation [ft]
    #p = pressure [psia]
    #t = temperature [degF]
    if outtype == 'p':
        res = 14.696*(1-(6.8754*10**(-6))*z)**5.2559;
    elif outtype == 't':
        res = 59 - 0.00356620*z;
        
    return res

def psychro(Tdb,p,humtype,humvalue,outtype):
    """
    created by: Matthew Simones, 12/5/2016
    Modified by: Matthew Simones, 2/7/2017
    NEED CHECK FOR Tdb > Twb, RH > 100%
    
    psychro returns the requested psychrometric property given dry bulb
    temperature (Tdb), absolute pressure (p), and humidity information 
    (Twb, RH, or W). Assume moist air as ideal gas, includes enhancement factor
    (f) for correction of vapor pressure of water
    
    options for humtype:
        'Twb' = thermodynamic wet bulb temperature [degF]
        'RH' = relative humidity [%]
        'W' = humidity ratio [lbm,w/lbm,da]
        
    options for outtype:
        'T' = dry bulb temperature [degF]
        'Twb' = thermodynamic wet bulb temperature [degF]
        'RH' = relative humidity [%]
        'W' = humidity ratio [lbm,w/lbm,da]
        'Ws' = humidity ratio at saturation [lbm,w/lbm,da]
        'mu' = degree of saturation [-]
        'pw' = partial pressure of water vapor [psia]
        'pws' = partial pressure of water vapor at saturation [psia]
        'h' = enthalpy [Btu/lbm,da]
        'cp' = specific heat capacity of moist air [Btu/(lbm,da degF)]
        'Tdp' = dew point temperature [degF]
        'v' = specific volume of dry air [Btu/lbm,da]
        'v_prime' = specific volume of moist air [Btu/lbm]
    """
    #---Constants---
    R = 1545.35; #universal gas constant [Btu/(lbmol degR)]
    Mda = 28.966; #molar mass of dry air [lbm/lbmol]
    Mw = 18.015268; #molar mass of water [lbm/lbmol]
    Rda = R/Mda; #gas constant of dry air [Btu/(lbm degR)]
    Rw = R/Mw; #gas constant of water vapor [Btu/(lbm degR)]
    f = 1.0044; #enhancement factor [-]
    
    #---Local Function Definitions---
    def fun_pws(T):
        #returns saturation pressure over liquid water (pws) [psia]
        #T = temperature [degF]
        #f = enhancement factor, corrects vapor pressure for presence of air molecules
    
        C1 = -1.0214165E+04;
        C2 = -4.8932428E+00;
        C3 = -5.3765794E-03;
        C4 = 1.9202377E-07;
        C5 = 3.5575832E-10;
        C6 = -9.0344688E-14;
        C7 = 4.1635019E+00;
        C8 = -1.0440397E+04;
        C9 = -1.1294650E+01;
        C10 = -2.7022355E-02;
        C11 = 1.2890360E-05;
        C12 = -2.4780681E-09;
        C13 = 6.5459673E+00;
        Tabs = T + 459.67;
        if (T < 32) & (T > -148):
            res = np.exp(C1/Tabs+C2+C3*Tabs+C4*Tabs**2+C5*Tabs**3+C6*Tabs**4+C7*np.log(Tabs));
        elif (T >= 32) & (T < 392):
            res = np.exp(C8/Tabs+C9+C10*Tabs+C11*Tabs**2+C12*Tabs**3+C13*np.log(Tabs));
        return f*res;
        
    def fun_RH(T,pv):
        #returns the relative humidity (RH) [%]
        #T = dry bulb temperature [degF]
        #pv = partial pressure of water vapor [psia]
        return 100.*pv/fun_pws(T)
    
    def fun_Ws(T,p):
        #returns the humidity ratio at saturation (Ws) [lbm,w/lbm,da]
        #T = temperature [degF]
        #p = absolute pressure [psia]
        return (Rda/Rw)*fun_pws(T)/(p-fun_pws(T))
        
    def fun_W(p,pv):
        #returns the humidity ratio [lbm,w/lbm,da]
        return (Rda/Rw)*pv/(p-pv)
        
    def fun_W_therm(Tdb,Twb,p):
        #returns the humidity ratio given the thermodynamic wet-bulb Temp. [lbm,w/lbm,da]
        #Tdb = dry-bulb temperature [degF]
        #Twb = wet-bulb temperature [degF]
        #p = absolute pressure [psia]
        if (Tdb > 32):
            res = ((1093 - 0.556*Twb)*fun_Ws(Twb,p) - 0.240*(Tdb-Twb))/(1093 + 0.444*Tdb - Twb);
        elif (Tdb <= 32):
            res = ((1220 - 0.4*Twb)*fun_Ws(Twb,p) - 0.240*(Tdb - Twb))/(1220 + 0.444*Tdb - 0.48*Twb);
        return res             
    
    def fun_pv(p,W):
        #return the vapor pressure of water given W [psia]
        #p = absolute pressure [psia]
        #W = humidity ratio [lbm,w/lbm,da]
        return p*W/((Rda/Rw)+W)
        
    def fun_pv_RH(pws,RH):
        #returns the vapor pressure of water given RH [psia]
        return RH*pws/(100.)
        
    def fun_Twb_therm(Tdb,W,p):
        err = 1;
        dT = 1E-03;
        Twb0 = Tdb;
        Twb1 = Tdb - dT;
        f0 = fun_W_therm(Tdb,Twb0,p)-W;
        f1 = fun_W_therm(Tdb,Twb1,p)-W;
        while (err > 1E-6):
            Twb2 = Twb1 - f1*(Twb1-Twb0)/(f1-f0);
            Twb0 = Twb1; Twb1 = Twb2;
            f0 = fun_W_therm(Tdb,Twb0,p)-W;
            f1 = fun_W_therm(Tdb,Twb1,p)-W;
            err = abs(f1-f0)/f1;
        return Twb2
    
    def fun_v(T,p,W):
        #returns the specific volume of moist air [ft^3/lbm,da]
        #Tdb = temperature [degF]
        #p = absolute pressure [psia]
        #W = humidity ratio [lbm,w/lbm,da]
        Tabs = T + 459.67; # degF -> degR
        return Rda*Tabs*(1+(Rw/Rda)*W)/(p*144)
    
    def fun_v_prime(v,W):
        #returns the specific volume of moist air [ft^3/lbm]
        return v/(1+W)
    
    def fun_ha(T,W):
        #returns enthalpy of moist air [Btu/lbm,da]
        #T = temperature [degF]
        #W = humidity ratio [lbm,w/lbm,da]
        return 0.240*T + W*(1061 + 0.444*T)
        
    def fun_cpa(W):
        #cpa = specific heat capacity of moist air [Btu/(lbm,da degR)]
        #W = humidity ratio [lbm,w/lbm,da]
        return 0.240 + 0.444*W
    
    def fun_Tdp(T,pv):
        alpha = np.log(pv);        
        C14 = 100.15;
        C15 = 33.193;
        C16 = 2.319;
        C17 = 0.17074;
        C18 = 1.2063;
        if (T < 32):
            res = 90.12 + 26.142*alpha + 0.8927*alpha**2;
        elif (T >= 32) & (T < 200):
            res = C14 + C15*alpha + C16*alpha**2 + C17*alpha**3 + C18*(pv)**0.1984;
        return res
        
    #---Calculations---
    #Determine thermodynamic wet-bulb temperature
    if (humtype == 'Twb'):
        Twb = humvalue;
    elif (humtype == 'RH'):
        Twb = fun_Twb_therm(Tdb,fun_W(p,fun_pv_RH(fun_pws(Tdb),humvalue)),p);
    elif (humtype == 'W'):
        Twb = fun_Twb_therm(Tdb, humvalue,p);
    
    #humidity ratio at saturation (Ws) [lbm,w/lbm,da]
    Ws = fun_Ws(Tdb,p)
    #humidity ratio (W) [lbm,w/lbm,da]
    W = fun_W_therm(Tdb,Twb,p);
    #degree of saturation [-]
    mu = W/Ws;
    #partial pressure of water vapor (pv) [psia]    
    pv = fun_pv(p,W);
    #sat. vapor pressure (pws) [psia]
    pws = fun_pws(Tdb);
    #relative humidity (RH) [%]
    RH = fun_RH(Tdb,fun_pv(p,fun_W_therm(Tdb,Twb,p)));
    #enthalpy (h) [Btu/(lbm,da degF)]
    h = fun_ha(Tdb,W);
    #specific heat capacity of moist air (cp) [Btu/(lbm,da degF)]
    cp = fun_cpa(W);
    #dew point (Tdp) [degF]
    Tdp = fun_Tdp(Tdb, pv);
    #specific volume (v) [ft^3/lbm,da]
    v = fun_v(Tdb,p,W);
    #specific volume (v') [ft^3/lbm]
    vprime = fun_v_prime(v,W);
    
    if (outtype == 'T'):
        outvalue = Tdb;
    elif (outtype == 'Twb'):
        outvalue = Twb;
    elif (outtype == 'RH'):
        outvalue = RH;
    elif (outtype == 'W'):
        outvalue = W;
    elif (outtype== 'Ws'):
        outvalue = Ws;
    elif (outtype == 'mu'):
        outvalue = mu;
    elif (outtype == 'pv'):
        outvalue = pv;
    elif (outtype == 'pws'):
        outvalue = pws;
    elif (outtype == 'h'):
        outvalue = h;
    elif (outtype == 'cp'):
        outvalue = cp;
    elif (outtype == 'Tdp'):
        outvalue = Tdp;
    elif (outtype == 'v'):
        outvalue = v;
    elif (outtype == 'vprime'):
        outvalue = vprime;
    
    return outvalue