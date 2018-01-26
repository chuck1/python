import math
import sys
import json
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

from blueprint import *

b = BlueprintBook.read(sys.argv[1])

b.find_print("4-way Junction").plot()



