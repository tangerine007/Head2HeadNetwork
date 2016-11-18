# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:02:10 2016

@author: Ben
"""
import random
from math import log, ceil, sqrt
from pandas import read_csv, concat
from scipy.stats import norm

#First create 'N' players in network:
#DONE - 1) Randomly assign them skill levels normal between 0-100 (mimic Microsoft TrueSkill)
#DONE - 2) Randomly assign them a region (out of 'R'available regions)
def generatePlayers(fileOut='players.csv',simulatedPlayersN=10000,regionR=4,localL=10,skillSigma=5):
    with open("Resources/"+fileOut,'w') as f:
        f.write("playerId,region,local,skillMean,skillSigma\n")
        for i in range(simulatedPlayersN):
            playerId=`i`
            region=`random.randint(1,regionR)`
            local=`random.randint(1,localL)`
            skillMean=`min(max(random.gauss(50,10),0),100)`
            skillSigmaToWrite=`random.uniform(skillSigma/2,skillSigma)`
            writeString = playerId+","+region+","+local+","+skillMean+","+skillSigmaToWrite+'\n'
            f.write(writeString)
            
#Generate 'G' games:
#1) Randomly generate many 'Local' tournaments with ~N/1000 players each in each region
#2) Randomly generate fewer 'Regional' tournaments with ~N/100 players each
#3) Randomly generate very few 'National' tournaments with ~N/10 players each ex. N=10,000, there will be ~1000 players
#**Make sure that few out of region players are at locals where more out of region players are at Regionals/Nationals
#**Use proper seeding based on skill levels
#**Make sure higher ranked players are more likely to be included in Regional/National tournaments
def seed(n):
    ol = [1]
    for i in range(int(ceil(log(n)/log(2)))):
        l = 2*len(ol) + 1
        ol = [e if e <= n else 0 for s in [[el, l-el] for el in ol] for e in s]
    return ol

def pWin(p1,p2):
    if type(p1)==int:
        return p2
    if type(p1)==int:
        return p1
    deltaMu = p1.skillMean - p2.skillMean
    rsss = sqrt(p1.skillSigma**2 + p2.skillSigma**2)
    return [p1,p2][norm.cdf(deltaMu/rsss)>random.random()]
    
    
    
def runTournament(tourneyPlayers):
    games=[]
    tourneyPlayers = tourneyPlayers.sort_values(by='skillMean',ascending=False)
    
    tourneySeed = [tourneyPlayers.iloc[i-1] if i>0 else 0 for i in seed(len(tourneyPlayers))]
    tourneySeed = map(None, *([iter(tourneySeed)] * 2))
    #Start with single elimination, add option for double elimination later?
    #for game in tourneySeed:
        
    

#Break down into Generating one tournament at a time, running them to collect the games
def generateLocalTournament(region,local,fileIn='players.csv',playerTravelIndex=.01):
    tourneySize=30
    players = read_csv("Resources/"+fileIn)
    nationalPlayers = players.query('region!='+`region`)
    regionPlayers = players.query('region=='+`region`+' and local!='+`local`)
    localPlayers = players.query('region=='+`region`+' and local=='+`local`)
    
    playerTypeList=[0,0,0]#local,regional,national
    for i in range(tourneySize):
        if random.random()<=playerTravelIndex**2:
            playerTypeList[2]+=1
        elif random.random()>=1-playerTravelIndex:
            playerTypeList[1]+=1
        else:
            playerTypeList[0]+=1

    if playerTypeList[2]>0 and len(nationalPlayers)>0:
        nationalPlayers = nationalPlayers.sample(n=playerTypeList[2])
    if playerTypeList[1]>0 and len(regionPlayers)>0:
        regionPlayers = regionPlayers.sample(n=playerTypeList[1])
    if playerTypeList[0]>0:
        localPlayers = localPlayers.sample(n=playerTypeList[0])
    
    tourneyPlayers = concat((localPlayers,regionPlayers,nationalPlayers))
    runTournament(tourneyPlayers)

    
    
#playerTravelIndex: % of a regional player entering in a local
#playerTravelIndex**2: % of a national player playing in a local
def generateTournaments(fileIn='players.csv',fileOut='tournaments.csv',playerTravelIndex=.01):
    players = read_csv("Resources/"+fileIn)
    regionsR = range(players['region'].max())
    localsL= range(players['local'].max())
    generateLocalTournament(region=1,local=1,fileIn='players.csv',playerTravelIndex=.01)
    #with open("Resources/"+fileOut,'w') as f:
        #f.write("GameId,playerId,region,skillMean,skillSigma\n")
       




#Run generated Tournaments:
#1) Create a likelyhood that a player will beat another player based on their difference in skill level (mimic Microsoft TrueSkill)
#2) Collect all games played and outcomes


#----------BELOW CAN BE USED IN A GENERAL SENSE TO TEST REAL DATA------------

#Build Training/Test sets:
#1) Collect one game from all players in the network
#2) From those games, if more games were played against the same opponent, grab all games played between the two players
#3) Randomly select more games (all games between two opponents included) until training is at 'train%'. These games will be added 
    #into the network
#4) The remaining games will be put in a separate pile 'test%' pile
#**for right now let's assume 'train%'=70% and 'test%'=30%

#Train/Test the model!:
#1) Train the network using your training set
#2) Based on the output pageranks for each player in the network, predict who will win all of the games in the test set
#3) Display the results



#RUN
generatePlayers(fileOut='players.csv',simulatedPlayersN=100,regionR=1,localL=1,skillSigma=0)
generateTournaments(fileIn='players.csv',fileOut='tournaments.csv',playerTravelIndex=.5)