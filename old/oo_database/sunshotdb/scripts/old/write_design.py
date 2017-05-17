# create a new object and add it to the database

import oodb


l = []

# ST (m)	SL (m)	SD (m)	D (m)	SE (m)	NL	NT	v_in (m/s)
data =[
    [4.00E-04,	1.1E-04,	2.28E-04,	1.00E-04,	2.00E-04,	18,	6,	0.638],
    [4.00E-04,	1.1E-04,	2.28E-04,	1.00E-04,	2.00E-04,	28,	6,	0.934],
    [4.00E-04,	1.1E-04,	2.28E-04,	1.00E-04,	2.00E-04,	38,	6,	1.229],
    [4.00E-04,	2.0E-04,	2.83E-04,	1.00E-04,	2.00E-04,	18,	6,	1.073],
    [4.00E-04,	2.0E-04,	2.83E-04,	1.00E-04,	2.00E-04,	28,	6,	1.610],
    [4.00E-04,	2.0E-04,	2.83E-04,	1.00E-04,	2.00E-04,	38,	6,	2.146],
    [4.00E-04,	4.0E-04,	4.47E-04,	1.00E-04,	2.00E-04,	18,	6,	2.039],
    [4.00E-04,	4.0E-04,	4.47E-04,	1.00E-04,	2.00E-04,	28,	6,	3.112],
    [4.00E-04,	4.0E-04,	4.47E-04,	1.00E-04,	2.00E-04,	38,	6,	4.185],
    [2.00E-04,	2.0E-04,	2.24E-04,	1.00E-04,	2.00E-04,	45,	8,	2.662],
    [2.00E-04,	2.0E-04,	2.24E-04,	1.00E-04,	1.50E-04,	49,	8,	2.897],
    [2.00E-04,	2.0E-04,	2.24E-04,	1.00E-04,	2.00E-04,	40,	8,	2.378],
    [2.00E-04,	2.0E-04,	2.24E-04,	1.00E-04,	1.00E-04,	49,	8,	2.897]
    ]

for dat in data:
    
    d = oodb.classes.Design(oodb.util.get_next_id())

    d.desc = 'pin'
    
    d.fluid_str = 'co2'
    d.qpp = 1e6
    d.temp_in = 773.15
    d.temp_out = 923.15

    d.height_channel = 2e-4
    d.width_wall = 1e-4
    d.length_in = 2e-4
    d.length_out = 2e-4
    d.height_front = 1e-4
    d.height_back = 1e-4

    d.ST = dat[0]
    d.SL = dat[1]
    d.D = dat[3]
    d.SE = dat[4]
    d.NL = dat[5]
    d.NT = dat[6]



    g = oodb.classes.Geo(oodb.util.get_next_id(), d.id)

    #g.desc = 'half channel'

    #g.number_of_channels_modeled = 0.5
    g.v_in = dat[7]

    l += [d,g]

oodb.util.save_to_next(l)

