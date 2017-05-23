# create a new object and add it to the database

import oodb

# Run	Span	Lamp Setting	Flow Meter (g/s)	Pressure (bar)
# Cold_Gas Out	    Preheated Gas	TA Inlet Gas	TA Inlet Gas (calibrated)   TA Outlet Gas	TA Outlet Gas (calibrated)
# Inlet_Flux	    Inlet Header	Outlet Flux	Outlet Header	TestSect_5
# Inlet_Tube_Wall	Outlet Tube Wall	PreHeater Surface	Reflector Surface
# Inlet_Side_Insu       Outlet_Side_Insu	Preheat to Preheater	Upstream Pressure (bar)

data = [
    [1,[30,32],0.82,0.6221276694,83.0836100956,33.4372932162,470.6570244678,415.7256307401,414.2519794786,666.3649355281,664.9689151377,640.9781717713,637.2495010125,703.6938589917,
     702.1543575967,	62.3666995343,	553.1765769709,	674.3398688067,	688.0390144033,	42.268217684,	2302.8408674615,	2302.8408674615,	7.0699863701,	84.7831243347,  334.7
     ],
    [2,[26,28],0.98,0.9097322328,81.1219100603,33.8058007110,439.4679519834,402.6171594241,401.1697251053,655.0865187983,653.7096717164,627.9347561185,618.1189569002,698.6610404241,
     692.1932441164,	30.8815054636,	533.5492211871,	660.7297390312,	673.561230447,	45.2041849356,	2300.6928185052,	2300.6928185052,	-5.259139185,	84.0635615301,  428.9
     ],
    [3,[31,33],0.70,0.4694392453,82.3782444283,32.6366456445,492.9962485281,419.0230142225,417.5427681940,654.4260295509,653.0503053007,636.4218713701,635.9965950936,690.5556037588,
     692.6233558482,	50.2664598524,	555.0510588274,	666.5653963326,	691.2402929418,	39.4425946674,	2304.0645740956,	2304.0645740956,	7.8285834511,	83.5475866507,  254.0
     ],
    [4,[39,41],0.70,0.7638563285,78.6769450333,33.4959017921,457.4680064200,412.3388311580,410.8719534957,575.1699784220,573.9289894587,555.3702191040,552.3890972204,602.1609193430,
     600.8069145759,	47.7466725800,	488.5225376985,	578.0695143056,	687.3845002121,	39.4273113992,	2303.838885027,         2303.8388850270,	2.8881935426,	80.9385801040,  254.0
     ],
    [5,[21,23],0.70,1.1852426570,78.3979093867,38.0446649272,414.1596651788,388.1252039252,386.7067535173,501.3980827069,500.2825059663,485.7698777464,480.2777204075,523.8394439875,
     520.7363702204,	18.7849387817,	431.1992687942,	500.5856968857,	681.4355243222,	39.9988432079,	2303.2960880811,	2303.2960880811,	-2.3282848607,	82.5882071143,  254.0
     ]
    ]

l = []

o = oodb.classes.HeatLossCurve(oodb.util.get_next_id(), 122)

o.ploy_fit_data = [0.0822, -9.4957]

o.desc = 'used for 7/9/2014 experimental data'

l += [o]

for d in data:
    e = oodb.classes.Experiment(oodb.util.get_next_id(), 122)

    e.desc = 'option 2; 2.2.a.3; data from 7/9/2014'
    
    e.heat_loss_curve_id = o.id
    
    e.run                               = d[0]
    e.time_span                         = d[1]
    e.lamp_setting                      = d[2]
    e.mass_flow_rate                    = d[3]
    e.pressure_outlet                   = d[4]
    
    e.temperature_cold_gas_out          = d[5]
    e.temperature_preheated_gas         = d[6]
    e.temperature_inlet                 = d[7]
    e.temperature_inlet_cal             = d[8]
    e.temperature_outlet                = d[9]
    e.temperature_outlet_cal            = d[10]
    e.temperature_inlet_flux            = d[11]
    e.temperature_inlet_header          = d[12]
    e.temperature_outlet_flux           = d[13]
    e.temperature_outlet_header         = d[14]
    e.temperature_testsect5             = d[15]
    e.temperature_inlet_tube_wall       = d[16]
    e.temperature_outlet_tube_wall      = d[17]

    e.temperature_preheater_surface     = d[18]
    e.temperature_reflector_surface     = d[19]
    
    e.temperature_inlet_side_insu       = d[20]
    e.temperature_outlet_side_insu      = d[21]
    
    e.temperature_preheat_to_preheater  = d[22]
    e.pressure_inlet                    = d[23]

    e.qpp_in                            = d[24]
    
    l += [e]



oodb.util.save_to_next(l)



