# --- Improvements ---

import requests
import csv
import pandas as pd
import sys
from colorama import Fore, Style
from difflib import get_close_matches
import math
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

makePlots = False
makeRosters = False

# List of owners with initialized rosters
owners = [["Blake  ",0,0,0,0], ["Brandon",0,0,0,0], ["Dexter ",0,0,0,0], ["Jordan ",0,0,0,0], ["Justin ",0,0,0,0], ["Kyle   ",0,0,0,0], ["Matt   ",0,0,0,0], ["Nick   ",0,0,0,0], ["Tristin",0,0,0,0], ["Tyler  ",0,0,0,0]]

# Ask for url or csv
print("")
type = input( "Using a url or csv? " )
print("")

# Get my rankings
if type == 'csv':
    # Uncomment to ask for csv name
    #filename = input( "What is the file name? " )
    #filename = 'myRankings.csv'
    filename = 'myRankings.csv'
    df = pd.read_csv(filename)

elif type == 'url':
    url = input( "What is the url? " )
    html = requests.get(url).content
    df_list = pd.read_html(html,header=0)
    df = df_list[-1]
    # Uncomment these lines to store data from url to csv 
    #df.to_csv(r'espnHPPR.csv')
    #sys.exit()

else:
    print( "incorrect type" )
    sys.exit()



for i in range (10000):
    
    # Get the player's name
    print("")
    name = input( "What player? " )
    print("")

    # To exit the loop
    if name == 'exit': sys.exit()

    # Find the row
    row = df.loc[df['NAME'] == name]

    # Get the value of the player
    price = str( row['$'] ).split()
    value = price[1].split('$')
    try: number = int( value[1] )
    except:
        options = get_close_matches(name,df['NAME'].values,3,0.6)
        try: name = options[0]
        except: continue
        row = df.loc[df['NAME'] == name]
        price = str( row['$'] ).split()
        value = price[1].split('$')
        number = int( value[1] )

    # Calculate the value variables
    steal = round( number - (number*0.2) )
    deal  = round( number - (number*0.1) )
    max   = round( number + (number*0.075) )

    # Print the variables for the player
    print("")
    print( "----- ", name, " -----" )
    print('\033[91m'+'max:   ',Style.RESET_ALL+'$',max)
    print('\033[37m'+'value: ',Style.RESET_ALL+'$', number)
    print('\033[92m'+'deal:  ',Style.RESET_ALL+'$',deal)
    print('\x1b[1m'+'\033[92m'+'steal: ',Style.RESET_ALL+'$',steal)
    print("")

    if makeRosters:
        #Get updated rosters
        owner_tmp = input("Who drafted " + name + "? ")
        pos = str( row['POS'] ).split()                                                                                                                          
        position = pos[1]
        for team in owners:
            if owner_tmp in team[0]:
                if position == 'QB': team[1] += 1
                elif position == 'RB': team[2] += 1
                elif position == 'WR': team[3] += 1
                elif position == 'TE': team[4] += 1
        

        print( "" )
        print( "------- Updated Rosters  -------" )

        # Print the updated rosters
        for team in owners:
            print( team[0], ":", team[1], "QBs,", team[2], "RBs,", team[3], "WRs,", team[4], "TEs" )



    if makePlots:
        # Make plot
        variance = max-deal
        if variance == 0: variance = 1
        sigma = math.sqrt(variance)

        x = np.linspace(number - 3*sigma, number + 3*sigma, 100)

        plt.plot(x, stats.norm.pdf(x, number, sigma))
        plt.ylim(bottom=0)
        y_mean = stats.norm.pdf(number, number, sigma)
        y_max = stats.norm.pdf(max, number, sigma)
        y_deal = stats.norm.pdf(deal, number, sigma)
        plt.vlines(x=number, color='k', ymin=0.0, ymax=y_mean, linewidth=1, linestyle='dashed' )
        plt.vlines(x=max, color='red', ymin=0.0, ymax=y_max, linewidth=1, linestyle='dashed' )
        plt.vlines(x=deal, color='green', ymin=0.0, ymax=y_deal, linewidth=1, linestyle='dashed' )
        plt.title(name)
        plt.show()
    

