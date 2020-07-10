# --- Improvements ---

import csv
import pandas as pd
import sys, os
import subprocess
from colorama import Fore, Style
from difflib import get_close_matches
import math
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from functions import getValues, getName, getRow, printVariables, makeRosters, plotRosters


owners = [["blake  ",0,0,2,0], ["brandon",0,1,1,0],
          ["dexter ",0,2,0,0], ["jordan ",1,0,1,0],
          ["justin ",0,2,0,0], ["kyle   ",1,1,0,0],
          ["matt   ",1,0,1,0], ["nick   ",0,0,2,0],
          ["tristin",0,1,1,0], ["tyler  ",0,2,0,0],
          ["dummy  ",2,7,7,2]]

df = getValues()


while True:
    name = getName()
    row, name, value = getRow(name,df)
    if name == 0: continue
    printVariables(name,value)
    if not makeRosters(row,name,owners):
        print('Not an owner. Try again!')
        continue
    
    plotRosters(owners)
            
    

