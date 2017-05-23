
from CoolProp.CoolProp import PropsSI

fluids = ["acetone",
"Ammonia",
"Argon",
"Bromine",
"Caesium",
"co2",
"Chlorine",
"ethane",
"ethanol",
"ethylene",
"Fluorine",
"Gold",
"Helium",
"Hydrogen",
"Krypton",
"Lithium",
"Mercury",
"methane",
"methanol",
"Neon",
"nitrogen",
"NitrousOxide",
"oxygen",
"propane",
"propylene",
"Sulfur",
"sulfuric acid",
"water",
"Xenon",]

for f in fluids:
    T = None
    P_t = None
    try:
        T = PropsSI("T", "P", 101300, "Q", 0, f)
    except: pass

    try:
        P_t = PropsSI("P_TRIPLE", f)
    except: pass

    print "{:16}{:24} {:24}".format(f,T,P_t)




