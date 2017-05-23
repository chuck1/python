
import networkx as nx

G=nx.DiGraph()

def add_edge(g, a, b, w):
    g.add_edge(a, b, weight=w)

def add_edge_bi(g, a, b, w):
    add_edge(g, a, b, w)
    add_edge(g, b, a, w)

G.add_edge(    "Kerbin",                "Low Kerbin Orbit",      weight=4550)

# Eve
add_edge_bi(G, "Kerbin SOI Edge",       "Eve Intercept",                 430+20)
add_edge_bi(G, "Eve Intercept",         "Elliptical Eve Orbit",           80)
add_edge_bi(G, "Elliptical Eve Orbit",  "Low Eve Orbit",                1330)

G.add_edge("Low Eve Orbit", "Eve", weight=0)
G.add_edge("Eve", "Low Eve Orbit", weight=12000)

# Gilly
add_edge_bi(G, "Elliptical Eve Orbit",  "Gilly Intercpt",   60)
add_edge_bi(G, "Gilly Intercpt",        "Low Gilly Orbit", 410)
add_edge_bi(G, "Low Gilly Orbit",       "Gilly",            30)


# Kerbin
add_edge_bi(G, "Kerbin SOI Edge",       "Low Kerbin Orbit",              950)
add_edge_bi(G, "Low Kerbin Orbit",      "High Kerbin Orbit",            1150)

# Mun
add_edge_bi(G, "Low Kerbin Orbit",      "Mun intercept",                 860)
add_edge_bi(G, "Mun intercept",         "Low Mun Orbit",                 310)
add_edge_bi(G, "Low Mun Orbit",         "Mun",                           580)

# Minmus
add_edge_bi(G, "Kerbin SOI Edge",       "Minmus intercept",               20 + 340)
add_edge_bi(G, "Low Kerbin Orbit",      "Minmus intercept",              930 + 340)
add_edge_bi(G, "Minmus intercept",      "Low Minmus Orbit",              160)
add_edge_bi(G, "Low Minmus Orbit",      "Minmus",                        180)

# Duna
add_edge_bi(G, "Kerbin SOI Edge",       "Duna intercept",                130 + 10)
add_edge_bi(G, "Duna intercept",        "Elliptical Duna Orbit",         250)
add_edge_bi(G, "Elliptical Duna Orbit", "Low Duna Orbit",                360)

G.add_edge(    "Low Duna Orbit",        "Duna",                  weight=   0)
G.add_edge(    "Duna",                  "Low Duna Orbit",        weight=1400)

# Ike
add_edge_bi(G, "Elliptical Duna Orbit", "Ike Intercept",          30)
add_edge_bi(G, "Ike Intercept",         "Low Ike Orbit",         180)
add_edge_bi(G, "Low Ike Orbit",         "Ike",                   390)

# Jool
add_edge_bi(G, "Kerbin SOI Edge",       "Jool Intercept",                 980+270)
add_edge_bi(G, "Jool Intercept",        "Elliptical Jool Orbit",          160)

# Laythe
add_edge_bi(G, "Elliptical Jool Orbit", "Laythe Intercept",               930)
add_edge_bi(G, "Laythe Intercept",      "Low Laythe Orbit",              1070)

G.add_edge(    "Low Laythe Orbit",      "Laythe",                 weight=   0)
G.add_edge(    "Laythe",                "Low Laythe Orbit",       weight=3200)

# Bop
add_edge_bi(G, "Elliptical Jool Orbit", "Bop Intercept",         220+2440)
add_edge_bi(G, "Bop Intercept",         "Low Bop Orbit",         900)
add_edge_bi(G, "Low Bop Orbit",         "Bop",                   220)

# Pol
add_edge_bi(G, "Elliptical Jool Orbit", "Pol Intercept",         160+700)
add_edge_bi(G, "Pol Intercept",         "Low Pol Orbit",         820)
add_edge_bi(G, "Low Pol Orbit",         "Pol",                   130)

# Tylo
add_edge_bi(G, "Elliptical Jool Orbit", "Tylo Intercept",        400)
add_edge_bi(G, "Tylo Intercept",        "Low Tylo Orbit",       1100)
add_edge_bi(G, "Low Tylo Orbit",        "Tylo",                 2270)

# Vall
add_edge_bi(G, "Elliptical Jool Orbit", "Vall Intercept",        620)
add_edge_bi(G, "Vall Intercept",        "Low Vall Orbit",        910)
add_edge_bi(G, "Low Vall Orbit",        "Vall",                  860)

# Duna
add_edge_bi(G, "Kerbin SOI Edge",        "Eeloo Intercept",       1140 + 1330)
add_edge_bi(G, "Eeloo Intercept",        "Low Eeloo Orbit",       1370)
add_edge_bi(G, "Low Eeloo Orbit",        "Eeloo",                  620)


def do_trip(g, l):
    for i in range(0,len(l)-1):
        print l[i] + " --> " + l[i+1]
        length = nx.dijkstra_path_length(g, l[i], l[i+1])
        print "    {} * 1.5 = {}".format(length, length * 1.5)


l = ["Low Kerbin Orbit", "High Kerbin Orbit", "Low Eve Orbit", "Gilly"]
l = ["Kerbin", "Kerbin SOI Edge", "Gilly"]
l = ["Kerbin SOI Edge", "Gilly", "Low Eve Orbit", "Kerbin SOI Edge"]

do_trip(G, l)

#import matplotlib.pyplot as plt
#nx.draw(G)
#plt.show()




