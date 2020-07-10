import requests
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

def rgb(list):
    new_list = [float(x)/float(265) for x in list]
    return new_list
    
myRed = (242,95,92)
myOrange = (254,94,65)
myYellow = (255,242,117)
myLightGreen = (91,186,11)
myGreen = (77,170,87)
myDarkGreen = (38,83,43)
myBlue = (53,129,184)
#colors_qt = [rgb(myRed), rgb(myLightGreen), rgb(myBlue)]
#colors_rw = [rgb(myRed), rgb(myOrange), rgb(myYellow), rgb(myLightGreen), rgb(myGreen), rgb(myDarkGreen), rgb(myBlue)]
colors_qt = ['red','limegreen','blue']
colors_rw = ['red','orange','yellow','lime','limegreen','forestgreen','blue']
myCM_qt = LinearSegmentedColormap.from_list('my_list', colors_qt, N=3)
myCM_rw = LinearSegmentedColormap.from_list('my_list', colors_rw, N=7)


def getValues():
    #print("")
    #type = input( "Using a url or csv? " )
    #print("")
    type = 'csv'
    if type == 'csv':
        filename = 'myRankings.csv'
        df = pd.read_csv(filename)    
    elif type == 'url':
        url = input( "What is the url? " )
        html = requests.get(url).content
        df_list = pd.read_html(html,header=0)
        df = df_list[-1]
    else:
        print( "incorrect type" )
        sys.exit()
    return df
        
def getName():
    print("")
    name = input( "What player? " )
    print("")
    if name == 'exit': sys.exit()
    if name == 'done':
        print('Nice draft!!')
        sys.exit()
    return name

def getRow(name,df):
    row = df.loc[df['NAME'] == name]
    try: value = int( row['$'] )
    except:
        options = get_close_matches(name,df['NAME'].values,3,0.6)
        try: name = options[0]
        except: return 0, 0, 0
        row = df.loc[df['NAME'] == name]
        value = int( row['$'] )
    return row, name, value

def calculateVariables(value):
    steal = round( value - (value*0.2) )
    deal  = round( value - (value*0.1) )
    maximum   = round( value + (value*0.075) )
    return steal, deal, maximum

def printVariables(name,value):
    steal, deal, maximum = calculateVariables(value)
    print("")
    print( "----- ", name, " -----" )
    print('\033[91m'+'max:   ',Style.RESET_ALL+'$',maximum)
    print('\033[37m'+'value: ',Style.RESET_ALL+'$', value)
    print('\033[92m'+'deal:  ',Style.RESET_ALL+'$',deal)
    print('\x1b[1m'+'\033[92m'+'steal: ',Style.RESET_ALL+'$',steal)
    print("")

def makeRosters(row,name,owners):
    owner_tmp = input("Who drafted " + name + "? ")
    pos = str( row['POS'] ).split()                                                                                                                          
    position = pos[1]
    options = get_close_matches(owner_tmp,[k[0] for k in owners],3,0.3)
    try: owner_tmp = options[0]
    except: return False
    print('')
    print("Adding to %s's team" % owner_tmp.replace(' ', '').capitalize())
    print('')
    for team in owners:
        if owner_tmp in team[0]:
            if position == 'QB': team[1] += 1
            elif position == 'RB': team[2] += 1
            elif position == 'WR': team[3] += 1
            elif position == 'TE': team[4] += 1
    return True

def makePlots(value):
    steal, deal, maximum = calculateVariables(value)
    variance = maximum-deal
    if variance == 0: variance = 1
    sigma = math.sqrt(variance)
    x = np.linspace(value - 3*sigma, value + 3*sigma, 100)
    plt.plot(x, stats.norm.pdf(x, value, sigma))
    plt.ylim(bottom=0)
    y_mean = stats.norm.pdf(value, value, sigma)
    y_max = stats.norm.pdf(maximum, value, sigma)
    y_deal = stats.norm.pdf(deal, value, sigma)
    plt.vlines(x=value, color='k', ymin=0.0, ymax=y_mean, linewidth=1, linestyle='dashed' )
    plt.vlines(x=maximum, color='red', ymin=0.0, ymax=y_max, linewidth=1, linestyle='dashed' )
    plt.vlines(x=deal, color='green', ymin=0.0, ymax=y_deal, linewidth=1, linestyle='dashed' )
    plt.title(name)
    plt.show()

def makeHistVec(l):
    hl = []
    for i, item in enumerate(l):
        for p in range(item): hl.append(i)
    return hl

def makeText(list,pos):
    for i, num in enumerate(list):
        if i == 10: return
        plt.text(pos+0.45, i+0.45, str(num))
    
def plotRosters(owners):
    q, r, w, t = [], [], [], []
    for owner in owners:
        for i, pos in enumerate(owner):
            if i == 0: continue
            if i == 1: q.append(pos)
            if i == 2: r.append(pos)
            if i == 3: w.append(pos)
            if i == 4: t.append(pos)
    hq, hr, hw, ht = makeHistVec(q), makeHistVec(r), makeHistVec(w), makeHistVec(t)
    fig, ax = plt.subplots()
    fig.canvas.draw()
    plt.hist2d(np.full(sum(q),0,dtype=int), hq, bins=[1,11], range=np.array([(0,1), (0,11)]), cmap=myCM_qt)
    plt.hist2d(np.full(sum(r),1,dtype=int), hr, bins=[1,11], range=np.array([(1,2), (0,11)]), cmap=myCM_rw)
    plt.hist2d(np.full(sum(w),2,dtype=int), hw, bins=[1,11], range=np.array([(2,3), (0,11)]), cmap=myCM_rw)
    plt.hist2d(np.full(sum(t),3,dtype=int), ht, bins=[1,11], range=np.array([(3,4), (0,11)]), cmap=myCM_qt)
    makeText(q,0), makeText(r,1), makeText(w,2), makeText(t,3)
    plt.title('Current Rosters', fontweight='bold', fontsize=16)
    plt.xlim(0,4), plt.ylim(0,10)
    ax.set_xticks( [0.5,1.5,2.5,3.5] )
    ax.set_xticklabels(['QB', 'RB', 'WR', 'TE'])
    ax.set_yticks( [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5] )
    ax.set_yticklabels(['Blake','Brandon','Dexter','Jordan','Justin','Kyle','Matt','Nick','Tristin','Tyler'])
    fig = plt.gcf()
    fig.set_size_inches(5.5, 10)
    plt.savefig('rosters.png', dpi=100)
    bashCommand = 'open rosters.png'
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()



            
    

