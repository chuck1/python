# create a new object and add it to the database

import oodb


l = []

# dp	T_awaheated	T_maxheated (K)	T_mfaoutlet (K)	T_awacontact (K)

data = [
    [38721.629,	        971.56976,  1067.2709,	936.52429,  939.99695,  12],
    [45523.102,	        968.25793,  1064.8988,	937.18573,  936.95563,  14],
    [56842.402,	        963.17578,  1056.5804,	923.2796,   0,          16],
    [1.91E+004,	        966.5,	    1063.0,	923.1,	    950.2,      18],
    [3.22E+004,	        965.8,	    1066.9,	922.9,	    949.5,      20],
    [4.99E+004,	        953.2,	    1052.2,	923.5,	    0.0,        22],
    [333.1,	        1051.0,	    1127,	929.4,	    0.0,        25],
    [771.5,             1012.0,	    1098,	929.3,	    0.0,        27],
    [1671.0,	        986.5,	    1078,	930.1,	    0.0,        29],
    [916.9,	        1012.0,	    1110,	929.4,	    0.0,        31],
    [2706.0,	        980.8,	    1094,	929.7,	    0.0,        33],
    [6028.0,	        963.5,	    1081,	929.3,	    0.0,        35],
    [3017.0,	        1011.0,	    1138,	929.5,	    0.0,        37],
    [8305.0,	        988.5,	    1116,	930.1,	    0.0,        39],
    [18540.0,	        977.6,	    1116,	930.3,	    0.0,        41],
    [21760.0,	        936.6,	    1000,	926.1,	    0.0,        43],
    [30270.0,	        923.1,	    1039,	926.7,	    897.5,      45],
    [13570.0,	        936.8,	    1051,	923.3,	    909.6,      47],
    [39800.0,	        915.3,	    1025,	926.6,	    890.4,      49]
    ]


for dat in data:

    s = oodb.classes.Simulation(oodb.util.get_next_id(), dat[5])


    s.dp = dat[0]
    s.temp_heated_awa = dat[1]
    s.temp_heated_max = dat[2]
    s.temp_out_mfa = dat[3]
    s.temp_contact_awa = dat[4]

    l.append(s)
    


oodb.util.save_to_next(l)
