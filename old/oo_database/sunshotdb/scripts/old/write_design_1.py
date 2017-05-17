# create a new object and add it to the database

import oodb

l = []

# desc w_ch w_w h_ch l_ch
data = [
   ['o2.m1.sa.v1', 'o2.m1.sa.v2', 'o2.m1.sa.v3', 'o2.m1.sb.v1', 'o2.m1.sb.v2', 'o2.m1.sb.v3',
    'o2.m2.sa.v1', 'o2.m2.sa.v2', 'o2.m2.sa.v3', 'o2.m2.sb.v1', 'o2.m2.sb.v2', 'o2.m2.sb.v3'],
   [300, 300, 300, 300, 300, 300,
    500, 500, 500, 500, 500, 500],
   [316, 638, 931, 316, 638, 931,
    526, 1000, 1667, 526, 1000, 1667],
   [110, 150, 180, 110, 150, 180,
    220, 280, 360, 220, 280, 360],
   [1, 1, 1, 1, 1, 1,
    2, 2, 2, 2, 2, 2]
    ]


for i in range(12):
    
    d = oodb.classes.Rectangular(oodb.util.get_next_id())

    # const

    d.width = 2e-2
    
    d.fluid_str = 'co2'
    
    # not const
    
    d.desc = 'rect ' + data[0][i]
    
    d.width_channel     = data[1][i] * 1e-6
    d.width_wall        = data[2][i] * 1e-6
    d.height_channel    = data[3][i] * 1e-6
    d.length_channel    = data[4][i] * 1e-2
    
    l += [d]

oodb.util.save_to_next(l)

